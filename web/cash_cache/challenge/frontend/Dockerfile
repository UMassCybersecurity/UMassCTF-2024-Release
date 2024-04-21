FROM nginx:stable-alpine-slim
COPY nginxproxy.conf /etc/nginx/nginxproxy.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80
ENTRYPOINT [ "/entrypoint.sh" ]