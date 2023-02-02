FROM postgres:15.0-bullseye

ENV TZ=Europe/London

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY docker/postgres/schema/movies_database.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
