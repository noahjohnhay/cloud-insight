FROM python:2.7-alpine

WORKDIR /app

COPY . /app

RUN python setup.py install

VOLUME /root/.aws

VOLUME /project

WORKDIR /project

ENTRYPOINT ["cloud-insight"]