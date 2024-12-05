from flask import Flask, jsonify
from binance.client import Client
import os

app = Flask(__name__)
client = Client(None, None)

@app.route('/')
def home():
    return "Binance Service is running!"

@app.route('/test')
def test():
    return {"status": "ok", "message": "Test endpoint working"}

@app.route('/top-coins')
def get_top_coins():
    try:
        tickers = client.get_ticker()
        usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
        return jsonify(usdt_pairs[:3])  # İlk 3 coin'i döndür
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
