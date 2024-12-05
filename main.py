from flask import Flask, jsonify
from binance.client import Client
import os

app = Flask(__name__)
client = Client(None, None, testnet=True)  # Test modu aktif

@app.route('/')
def home():
    return "Binance Service is running!"

@app.route('/price/btc')
def get_btc_price():
    try:
        btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
        return jsonify(btc_price)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
