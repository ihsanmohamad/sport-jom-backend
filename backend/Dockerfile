FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY requirements.txt ./requirements.txt

COPY ./app /app

RUN pip install --no-cache-dir fastapi

RUN pip install -r requirements.txt