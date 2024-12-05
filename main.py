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
        if response.status_code == 200:
            data = response.json()
            usdt_pairs = []
            for coin in data:
                if coin['symbol'].endswith('USDT'):
                    usdt_pairs.append({
                        'symbol': coin['symbol'],
                        'price': coin['lastPrice'],
                        'change_24h': coin['priceChangePercent'],
                        'volume': coin['volume']
                    })
            return jsonify(usdt_pairs[:10])  # İlk 10 coin
        else:
            return {"status": "error", "message": "API error"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
