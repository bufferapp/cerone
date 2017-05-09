# This is based on the amazon_kclpy sample file in the Python KCL repository:
# https://github.com/awslabs/amazon-kinesis-client-python

from __future__ import print_function

import sys
import time

from amazon_kclpy import kcl
from amazon_kclpy.v2 import processor


def process_stream(processing_function):
    """Apply a function to the stream."""
    processor = RecordProcessor(processing_function)
    kcl_process = kcl.KCLProcess(processor)
    kcl_process.run()


class RecordProcessor(processor.RecordProcessorBase):
    """A RecordProcessor processes data from a shard in a stream."""
    def __init__(self, processing_function=None):
        self.SLEEP_SECONDS = 5
        self.CHECKPOINT_RETRIES = 5
        self.CHECKPOINT_FREQ_SECONDS = 60
        self.largest_seq = (None, None)
        self.last_checkpoint_time = None
        self.processing_function = processing_function

    def initialize(self, initialize_input):
        """Called once by a KCLProcess before any calls to process_records.

        Parameters
        ----------
        initialize_input : amazon_kclpy.messages.InitializeInput
            Information about the lease that this record processor has been
            assigned.
        """
        self.largest_seq = (None, None)
        self.last_checkpoint_time = time.time()

    def checkpoint(self, checkpointer,
                   sequence_number=None,
                   sub_sequence_number=None):
        """Checkpoints with retries on retryable exceptions.

        Parameters
        ----------
        checkpointer : amazon_kclpy.kcl.Checkpointer
            The checkpointer provided to either process_records
            or shutdown.
        sequence_number : str or None
            Sequence number to checkpoint at.
        sub_sequence_number : int or None
            Sub sequence number to checkpoint at.
        """
        for n in range(0, self.CHECKPOINT_RETRIES):
            try:
                checkpointer.checkpoint(sequence_number, sub_sequence_number)
            except kcl.CheckpointError as e:
                # A ShutdownException indicates that this record processor
                # should be shutdown. This is due to some failover event, e.g.
                # another MultiLangDaemon has taken the lease for this shard.
                if 'ShutdownException' == e.value:
                    sys.stderr.write('Shutdown Exception, skipping checkpoint')

                # A ThrottlingException indicates that one of our dependencies
                # is is over burdened, e.g. too many dynamo writes. We will
                # sleep temporarily to let it recover.
                elif 'ThrottlingException' == e.value:
                    if self.CHECKPOINT_RETRIES - 1 == n:
                        sys.stderr.write('Failed to checkpoint after {} \
                                         attempts, giving up'.format(n))
                    else:
                        sys.stderr.write('Was throttled while checkpointing, \
                                          will attempt again in {} seconds'
                                         .format(self.SLEEP_SECONDS))
                elif 'InvalidStateException' == e.value:
                    sys.stderr.write('MultiLangDaemon reported an invalid \
                                      state while checkpointing.')
                else:
                    sys.stderr.write('Encountered an error while \
                                      checkpointing, error was {e}.'
                                     .format(e=e))
            time.sleep(self.SLEEP_SECONDS)

    def process_record(self, data, partition_key,
                       sequence_number, sub_sequence_number):
        """Called for each record that is passed to process_records.

        Parameters
        ----------
        data : str
            The blob of data that was contained in the record.
        partition_key : str
            The key associated with this recod.
        sequence_number : int
            The sequence number associated with this record.
        sub_sequence_number : int
            the sub sequence number associated with this record.
        """
        try:
            self.processing_function(data,
                                     partition_key=partition_key,
                                     sequence_number=sequence_number)
        except Exception as e:
            sys.stderr.write('Error processing the data.')

    def should_update_sequence(self, sequence_number, sub_sequence_number):
        """Determines whether a new larger sequence number is available.

        Parameters
        ----------
        sequence_number : int
            The sequence number from the current record.
        sub_sequence_number : int
            The sub sequence number from the current record.
        Returns
        -------
        boolean
            True if the largest sequence should be updated, false otherwise.
        """
        return self.largest_seq == (None, None) or sequence_number > self.largest_seq[0] or (sequence_number == self.largest_seq[0] and sub_sequence_number > self.largest_seq[1])

    def process_records(self, process_records_input):
        """Process a list of records.

        Called by a KCLProcess with a list of records to be processed and a
        checkpointer which accepts sequence numbers from the records to
        indicate where in the stream to checkpoint.

        process_records_input : amazon_kclpy.messages.ProcessRecordsInput
            The records, and metadata about the records.
        """
        try:
            for record in process_records_input.records:
                data = record.binary_data
                seq = int(record.sequence_number)
                sub_seq = record.sub_sequence_number
                key = record.partition_key
                self.process_record(data, key, seq, sub_seq)
                if self.should_update_sequence(seq, sub_seq):
                    self.largest_seq = (seq, sub_seq)

            # Checkpoints every self.CHECKPOINT_FREQ_SECONDS seconds
            checkpoint_diff = time.time() - self.last_checkpoint_time
            if checkpoint_diff > self.CHECKPOINT_FREQ_SECONDS:
                self.checkpoint(process_records_input.checkpointer, str(self.largest_seq[0]), self.largest_seq[1])
                self.last_checkpoint_time = time.time()

        except Exception as e:
            sys.stderr.write("Encountered an exception while processing \
                              records. Exception was {e}\n".format(e=e))

    def shutdown(self, shutdown_input):
        """Handles the RecordProcessor shutdown step.

        Called by a KCLProcess instance to indicate that this record processor
        should shutdown. After this is called, there will be no more calls to
        any other methods of this record processor.

        As part of the shutdown process you must inspect shutdown_input.reason
        to determine the steps to take.

            - Shutdown Reason ZOMBIE:
                A record processor will be shutdown if it loses its lease.
                In this case the KCL will terminate the record processor. It is
                not possible to checkpoint once a record processor has lost its
                lease.
            - Shutdown Reason TERMINATE:
                A record processor will be shutdown once it reaches the end of
                a shard.  A shard ending indicates that it has been either
                split into multiple shards or merged with another shard. To
                begin processing the new shard(s) it's required that a final
                checkpoint occurs.

        shutdown_input : amazon_kclpy.messages.ShutdownInput
            Information related to the shutdown request
        """
        try:
            if shutdown_input.reason == 'TERMINATE':
                # Checkpointing with no parameter will checkpoint at the
                # largest sequence number reached by this processor on this
                # shard id
                sys.stderr.write('Was told to terminate, \
                                  will attempt to checkpoint.')
                self.checkpoint(shutdown_input.checkpointer, None)
            else:
                sys.stderr.write('Shutting down due to failover. \
                                  Will not checkpoint.')
        except:
            sys.stderr.write('Error shuting down the record processor.')
