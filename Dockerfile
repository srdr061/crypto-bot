FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

# Startup probe için bekleme süresi
ENV GUNICORN_CMD_ARGS="--timeout 3600 --workers 8 --preload"

CMD exec gunicorn main:app
