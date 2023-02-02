FROM nginx:1.23.2-alpine

ENV TZ=Europe/London

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apk update \
    && apk upgrade

COPY docker/nginx/config /etc/nginx/

EXPOSE 80
