from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Binance Service is running!"

@app.route('/test')
def test():
    return {"status": "ok", "message": "Test endpoint working"}

@app.route('/top-coins')
def get_top_coins():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/24hr')
        data = response.json()
        usdt_pairs = [t for t in data if t['symbol'].endswith('USDT')]
        return jsonify(usdt_pairs[:3])
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
