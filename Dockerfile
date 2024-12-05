FROM python:3.9-slim

# System dependencies
RUN apt-get update && \
    apt-get install -y build-essential wget pkg-config cmake && \
    rm -rf /var/lib/apt/lists/*

# Install TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.4.0-src.tar.gz ta-lib/

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

CMD exec gunicorn --workers 4 --timeout 3600 main:app
