FROM golang:1.21-bullseye as builder
WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY lib lib
COPY main.go .
RUN go build -o app

FROM ubuntu:22.04 as chroot
RUN mkdir /app
WORKDIR /app
COPY --from=builder /app/app .
RUN mkdir /home/haylin
COPY files/ /home/haylin/
RUN useradd -ms /bin/bash haylin
RUN chown -R haylin:haylin /home/haylin
RUN chmod 755 -R /home/haylin/*


RUN useradd -u 1337 -ms /bin/bash ftp

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb
COPY --from=chroot / /chroot
COPY nsjail.cfg  /home/user/
CMD kctf_setup && \
    (kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /app/app)

