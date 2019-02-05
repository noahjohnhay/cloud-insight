FROM python:2.7-alpine

WORKDIR /app

COPY . /app

RUN set -x && \
    apk add --update libintl && \
    apk add --virtual build_deps gettext && \
    cp /usr/bin/envsubst /usr/local/bin/envsubst && \
    apk del build_deps && \
    python setup.py install

VOLUME /root/.aws

VOLUME /app

EXPOSE 54321

ENTRYPOINT ["cloud-insight"]
