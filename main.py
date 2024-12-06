from flask import Flask
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
        
        usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
        sorted_pairs = sorted(
            usdt_pairs,
            key=lambda x: float(x['volume']),
            reverse=True
        )[:50]
        
        return [{'symbol': p['symbol'], 'volume': float(p['volume'])} for p in sorted_pairs]
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
