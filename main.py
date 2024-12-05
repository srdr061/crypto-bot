from flask import Flask
from binance.client import Client
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Binance Service is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
