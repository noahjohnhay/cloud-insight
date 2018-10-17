FROM python:2.7-alpine

WORKDIR /app

COPY . /app

RUN python setup.py install

RUN chmod 777 -R /app

VOLUME /root/.aws

VOLUME /app

ENTRYPOINT ["cloud-insight"]