FROM python:3.9-slim

# System dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    wget \
    pkg-config \
    cmake \
    libta-lib0 \
    libta-lib-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install numpy && \
    pip install -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

CMD exec gunicorn --workers 4 --timeout 3600 main:app
