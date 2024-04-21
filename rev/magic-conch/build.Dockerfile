FROM ubuntu:latest
RUN apt-get update && \
    apt-get install -y \
    make \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY challenge/src/ /home/user/

RUN make -f /home/user/src/Makefile

RUN chown -R 1337 /home/user/