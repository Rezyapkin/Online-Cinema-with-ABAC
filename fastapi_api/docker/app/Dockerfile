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
    PIP_DEFAULT_TIMEOUT=100

# setup environment
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && groupadd -g "${GID}" -r web \
    && useradd -d /opt/app -r -l -u "${UID}" -g web web \
    && chown web:web -R /opt/app

COPY requirements.txt requirements.txt

# install python deps
RUN pip install --no-cache-dir --upgrade pip==22.3 \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env.dist .env

USER web

EXPOSE 8000
