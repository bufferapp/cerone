#!/usr/bin/env bash

set -eu  # Check for undefined variables

# Java JARs location
JARSPATH=/usr/local/lib/python3.6/site-packages/amazon_kclpy/jars/

# Command generated from amazon_kclpy_helper.py
${JAVA_HOME}/bin/java -cp \
${JARSPATH}amazon-kinesis-client-1.7.5.jar:\
${JARSPATH}aws-java-sdk-cloudwatch-1.11.115.jar:\
${JARSPATH}aws-java-sdk-core-1.11.115.jar:\
${JARSPATH}aws-java-sdk-dynamodb-1.11.115.jar:\
${JARSPATH}aws-java-sdk-kinesis-1.11.115.jar:\
${JARSPATH}aws-java-sdk-kms-1.11.115.jar:\
${JARSPATH}aws-java-sdk-s3-1.11.115.jar:\
${JARSPATH}commons-codec-1.9.jar:\
${JARSPATH}commons-lang-2.6.jar:\
${JARSPATH}commons-logging-1.1.3.jar:\
${JARSPATH}guava-18.0.jar:\
${JARSPATH}httpclient-4.5.2.jar:\
${JARSPATH}httpcore-4.4.4.jar:\
${JARSPATH}ion-java-1.0.2.jar:\
${JARSPATH}jackson-annotations-2.6.0.jar:\
${JARSPATH}jackson-core-2.6.6.jar:\
${JARSPATH}jackson-databind-2.6.6.jar:\
${JARSPATH}jackson-dataformat-cbor-2.6.6.jar:\
${JARSPATH}jmespath-java-1.11.115.jar:\
${JARSPATH}joda-time-2.8.1.jar:\
${JARSPATH}protobuf-java-2.6.1.jar:\
/app \
com.amazonaws.services.kinesis.multilang.MultiLangDaemon \
main.properties
