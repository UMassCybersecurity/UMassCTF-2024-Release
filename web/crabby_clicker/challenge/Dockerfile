FROM golang:1.21-bullseye as builder
WORKDIR /app
COPY go.mod .
COPY main.go .
RUN go build -o app

FROM ubuntu:22.04 as chroot
RUN /usr/sbin/useradd --no-create-home -u 1337 user
COPY --from=builder /app/app /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb
COPY --from=chroot / /chroot
COPY nsjail.cfg  /home/user/
ENV FLAG="y_w0uld_u_w4nt_mult1p13_r3qu35t5"
CMD kctf_setup && \
    (kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/user/app)

