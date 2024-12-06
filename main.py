from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "API is running"

@app.route('/top-coins')
def get_top_coins():
    try:
        # Using the correct Binance API endpoint we used before
        ticker_url = 'https://data-api.binance.vision/api/v3/ticker/price'
        response = requests.get(ticker_url)
        tickers = response.json()
        
        usdt_pairs = []
        for ticker in tickers:
            if ticker['symbol'].endswith('USDT'):
                usdt_pairs.append({
                    'symbol': ticker['symbol'],
                    'price': float(ticker['price'])
                })
        
        sorted_pairs = sorted(usdt_pairs, key=lambda x: x['price'], reverse=True)[:50]
        return jsonify(sorted_pairs)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
