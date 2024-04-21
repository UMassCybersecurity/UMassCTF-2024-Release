#!/bin/sh

envsubst '${BACKEND_URL}' < /etc/nginx/nginxproxy.conf  >  /etc/nginx/nginx.conf
nginx -c nginx.conf -g 'daemon off;'