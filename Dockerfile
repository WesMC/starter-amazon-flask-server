FROM ubuntu:xenial

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
apt-get install -y python3 \
python3-pip

RUN pip3 install \
Werkzeug \
Jinja2 \
Flask \
prometheus_client

COPY . /src
