#!/usr/bin/env python

import json
from cerone import process_stream


def your_processing_function(data, partition_key=None, sequence_number=None):
    """Write the data to a file."""
    with open('data.json', 'a') as f:
        f.write("{}\n".format(json.dumps(data)))


if __name__ == "__main__":
    process_stream(your_processing_function)
