FROM python:3.11

LABEL authors="anastasiagusak"

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["bash", "-c", "while ! nc -z postgres 5432; do sleep 1; done; uvicorn app.main:app --host 0.0.0.0 --port 8080"]