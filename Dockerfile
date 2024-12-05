FROM python:3.9-slim

# TA-Lib dependencies
RUN apt-get update && apt-get install -y wget build-essential
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

CMD exec gunicorn --workers 1 --timeout 600 main:app
