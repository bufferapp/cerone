FROM python:3.6

# Install normal dependencies and OpenJDK JRE
RUN echo 'deb http://deb.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre

# See https://github.com/docker-library/java/issues/19#issuecomment-70546872
ENV CA_CERTIFICATES_JAVA_VERSION 20161107~bpo8+1

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        openjdk-8-jre-headless \
        ca-certificates-java="$CA_CERTIFICATES_JAVA_VERSION" \
        && rm -rf /var/lib/apt/lists/*

RUN pip install git+https://github.com/bufferapp/cerone

COPY entrypoint.sh /opt/entrypoint.sh
WORKDIR /app

CMD ["bash", "/opt/entrypoint.sh"]
