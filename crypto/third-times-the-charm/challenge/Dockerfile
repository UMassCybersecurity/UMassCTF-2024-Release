FROM python:3.10-slim-bookworm as chroot
RUN /usr/sbin/useradd --no-create-home -u 1337 user
RUN pip install pycryptodome
COPY ./src/* /home/user/

RUN chown -R 1337 /home/user/

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb
COPY --from=chroot / /chroot
COPY nsjail.cfg  /home/user/
CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /bin/bash /home/user/start.sh"