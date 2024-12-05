from flask import Flask
from binance.client import Client
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Binance Service is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
