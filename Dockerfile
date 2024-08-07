FROM python:3.11-slim-bookworm


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

EXPOSE 8087