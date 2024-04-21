FROM python:alpine3.19
RUN apk update
RUN apk add build-base supervisor npm

RUN pip install redis

RUN addgroup -S cash_group && adduser -S cash_user -G cash_group

COPY flag.txt /flag.txt
WORKDIR /app
COPY server/package.json .
RUN npm i
COPY config/supervisord.conf /supervisord.conf
COPY server .
WORKDIR /cache
COPY cache .
EXPOSE 9000

CMD [ "supervisord","-c","/supervisord.conf" ]