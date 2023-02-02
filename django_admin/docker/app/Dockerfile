FROM python:3.10.8-slim-bullseye

WORKDIR /opt/app

ENV TZ=Europe/London \
    # user, can be passed via ARGS:
    GID=1000 \
    UID=1000 \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # uwsgi
    UWSGI_PROCESSES=8 \
    UWSGI_THREADS=16 \
    UWSGI_HARAKIRI=60 \
    DJANGO_SETTINGS_MODULE='server.settings'

# setup environment
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends  \
      libpq-dev=13.9-0+deb11u1 \
      gcc=4:10.2.1-1 \
      # build-essential is needed for uwsgi wheel build
      build-essential=12.9 \
      make=4.3-4.1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY docker/app/uwsgi/uwsgi.ini uwsgi.ini
COPY docker/app/entrypoint.sh entrypoint.sh

# setup rootless user and django dirs
RUN mkdir -p /opt/app/static \
    && mkdir -p /opt/app/media \
    && groupadd -g "${GID}" -r web \
    && useradd -d /opt/app -r -l -u "${UID}" -g web web \
    && chown web:web -R /opt/app \
    && chmod +x ./entrypoint.sh

COPY requirements.txt requirements.txt

# install python deps
RUN pip install --no-cache-dir --upgrade pip==22.3 \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env.dist .env

USER web

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
