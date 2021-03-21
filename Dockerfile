FROM python:3.8-slim-buster

ARG user=okv
ARG group=okv
ARG uid=10000
ARG gid=10000

RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user} && \
    mkdir /okv && \
    chown -R ${uid}:${gid} /okv
WORKDIR /okv

COPY --chown=${uid}:${gid} entrypoint.sh .
# Should convert image to a multi-stage build and optimize
# for size later but this is for the POC
COPY --chown=${uid}:${gid} . .

RUN python setup.py install

USER ${user}

ENTRYPOINT [ "/okv/entrypoint.sh" ]