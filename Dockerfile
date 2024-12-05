FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

# Health check için startup süresini artır
ENV GUNICORN_TIMEOUT=3600
ENV WORKERS=8

CMD exec gunicorn --bind :$PORT --workers $WORKERS --timeout $GUNICORN_TIMEOUT main:app
