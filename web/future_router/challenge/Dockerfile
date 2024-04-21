FROM python:3.10-slim-bookworm as chroot
RUN /usr/sbin/useradd --no-create-home -u 1337 sheldonjplankton
RUN echo "UMASS{W3lC0m3_t0_Th3_FuTur3_Kr4bS_c28e1089b2}" > /flag53958e73c5ba4a66

RUN apt update
RUN pip3 install flask gunicorn pycurl websockets

WORKDIR /planktonsrouter1ba8b69e
COPY app/router .
COPY app/entrypoint.sh /

FROM nginx as nginxchroot
RUN /usr/sbin/useradd --no-create-home -u 1337 user
COPY nginx/nginx.conf  /etc/nginx/nginx.conf 
COPY nginx/nginx.sh /nginx.sh
RUN chown -R 1337 /etc/nginx

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends nginx \
    && ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && rm -rf /var/lib/apt/lists/*

COPY --from=chroot / /chroot
COPY --from=nginxchroot / /nginxchroot
COPY nginx  /home/user/nginx/

COPY app/nsjail.cfg /home/user/

CMD kctf_setup \
    && ((kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /bin/sh /entrypoint.sh)&) \
    && (kctf_drop_privs nsjail --config /home/user/nginx/nginx.nsjail.cfg -- /bin/sh /nginx.sh)
