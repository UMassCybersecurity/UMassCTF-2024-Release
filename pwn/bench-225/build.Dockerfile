FROM ubuntu:latest
RUN apt-get update && \
    apt-get install -y \
    make \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/tmp_bench_225/
COPY challenge/src/* /home/tmp_bench_225/

RUN make -f /home/tmp_bench_225/Makefile

RUN chown -R 1337 /home/tmp_bench_225/
