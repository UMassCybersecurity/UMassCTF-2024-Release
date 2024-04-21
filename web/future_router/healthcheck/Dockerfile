FROM gcr.io/kctf-docker/healthcheck@sha256:6709709a8cfd6e2d743c86d58398c00ca4eb26befd3b1a0a629ab35f91e98ef0

ENV BUILD_PACKAGES python3-pip build-essential python3-dev

RUN apt-get update \
    && apt-get -yq --no-install-recommends install $BUILD_PACKAGES \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install websockets \
    && apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto)

RUN apt-get update && apt-get -yq --no-install-recommends install cpio openssl python3 && rm -rf /var/lib/apt/lists/*

COPY healthcheck_loop.sh healthcheck.py healthz_webserver.py /home/user/

CMD kctf_drop_privs /home/user/healthcheck_loop.sh & /home/user/healthz_webserver.py
