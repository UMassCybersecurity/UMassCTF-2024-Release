FROM magic-conch-base as chroot
FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb
COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/
# CMD kctf_setup \
#     && bash -c 'ls -R /chroot/home/magic_conch_user'
CMD kctf_setup \
    && (kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/magic_conch_user/static/magic_conch)
