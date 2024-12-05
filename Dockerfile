FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

CMD exec gunicorn --workers 1 --timeout 0 main:app
