from flask import Flask, jsonify
from binance.client import Client
import os

app = Flask(__name__)
client = Client(None, None)

@app.route('/')
def home():
    return "Binance Service is running!"

@app.route('/coins')
def get_all_coins():
    try:
        tickers = client.get_all_tickers()
        usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
        return jsonify(usdt_pairs[:5])  # İlk 5 coin
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
