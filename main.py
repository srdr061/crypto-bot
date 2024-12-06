from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "API is running"

@app.route('/top-coins')
def get_top_coins():
    try:
        ticker_url = 'https://api.binance.com/api/v3/ticker/24hr'
        tickers = requests.get(ticker_url).json()
        
        # Dict yerine list kullanıyoruz
        usdt_pairs = []
        for ticker in tickers:
            if isinstance(ticker, dict) and ticker.get('symbol', '').endswith('USDT'):
                usdt_pairs.append({
                    'symbol': ticker['symbol'],
                    'volume': float(ticker['volume'])
                })
        
        # Hacme göre sırala
        sorted_pairs = sorted(usdt_pairs, key=lambda x: x['volume'], reverse=True)[:50]
        return jsonify(sorted_pairs)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
