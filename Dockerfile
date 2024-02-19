from python:3.9-slim

WORKDIR /workspace

RUN python3 -m venv venv
RUN venv/bin/pip install -U pip setuptools
RUN venv/bin/pip install poetry

COPY . /workspace

RUN poetry install --with mac
RUN poetry shell
RUN dvc pull -r trainremote data/train.zip
RUN dvc pull -r testremote data/test.zip
