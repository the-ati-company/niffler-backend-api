FROM python:3.11-slim-bookworm


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY api api
COPY src src
COPY firestore-service-account.json firestore-service-account.json


EXPOSE 8087