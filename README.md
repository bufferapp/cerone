# Cerone

Extensible consumer made for applications using [Amazon's Kinesis Python Client Library (KCL)](https://github.com/awslabs/amazon-kinesis-client-python).

## Installation

You can use `pip` to install Cerone.

```bash
pip install git+https://github.com/bufferapp/cerone
```

If you prefer, you can clone it and run the setup.py file. Use the following
commands to install Cerone from Github:

```bash
git clone https://github.com/bufferapp/cerone
cd cerone
python setup.py install
```

## Requirements

Cerone uses and communicates with the [Kinesis Client Library MultiLangDaemon](https://docs.aws.amazon.com/streams/latest/dev/developing-consumers-with-kcl.html#kinesis-record-processor-overview-kcl) interface. You can found the installation instructions in the [Amazon Kinesis Client Python repository](https://github.com/awslabs/amazon-kinesis-client-python#running-the-sample).

## Usage

Once you've defined the function you want to apply to the stream records, you can call Cerone's `process_stream`:

```python
from cerone import process_stream


def your_processing_function(record):
    with open('file.json', 'w') as f:
        f.write("{}\n".format(record))


if __name__ == "__main__":
    process_stream(your_processing_function)

```
