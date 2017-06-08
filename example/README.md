# Kinesis Consumer Example

This folder contains an example on how to build a consumer application using Cerone, Docker and a custom function.

## Requirements

The [Kinesis Client Library for Python](https://github.com/awslabs/amazon-kinesis-client-python) will try to grab the AWS using `DefaultAWSCredentialsProviderChain`. You should pass `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables to your Docker image.

### Files

The Docker image will need two files in `/app`:

- `main.py`: The `MultiLangDaemon` will call this script. We'll run the `processing_function` for all the records in the stream.
- `main.properties`: Stream related configuration.

## Usage

You can add `requirements.txt` as shown in this example. Once you've coded your function, build a Docker image using `bufferapp/cerone-consumer:0.1.1` as the base. In our case:

```bash
docker build -t cerone-sample-consumer .
```

Then, simply run the image with the required environment variables:

```bash
docker run -it --rm --env-file .env cerone-sample-consumer
```
