FROM python:3.11-slim-bookworm


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY api api
COPY src src
COPY service-account.json service-account.json


EXPOSE 80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]