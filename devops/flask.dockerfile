ARG DEPS_IMAGE=deps
FROM python:3.10-slim AS deps

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y \
    build-essential \
    curl \
    unzip \
    libssl-dev \
    python-dev \
    libpq-dev \
    libffi-dev \
    locales \
    python3-cffi \
    postgresql-client \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info\
    libpoppler-cpp-dev \
    pkg-config \
    libgeos-dev
#RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
#    && unzip awscliv2.zip \
#    && ./aws/install

# for pudb so it doesn't complaint it can't write it's settings
ENV XDG_CONFIG_HOME='/tmp/'

ENV POETRY_VERSION=1.1.12

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry config installer.parallel true && poetry install

#### Start of Code image ####

FROM ${DEPS_IMAGE} AS fraver

ENV FLASK_APP=/climbing/__init__.py
ENV PYTHONPATH=/climbing

ARG VERSION
ENV VERSION=${VERSION}
SHELL ["/bin/bash", "-c"]

COPY . /climbing
WORKDIR /climbing
