from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "API is running"

@app.route('/top-coins')
def get_top_coins():
    try:
        # Debug için print ekleyelim
        print("Fetching data from Binance...")
        
        response = requests.get('https://api.binance.com/api/v3/ticker/24hr')
        print(f"Response status: {response.status_code}")
        
        tickers = response.json()
        print(f"Total tickers: {len(tickers)}")
        
        usdt_pairs = []
        for ticker in tickers:
            if ticker['symbol'].endswith('USDT'):
                usdt_pairs.append({
                    'symbol': ticker['symbol'],
                    'volume': float(ticker['quoteVolume'])  # quoteVolume kullanıyoruz
                })
        
        print(f"USDT pairs found: {len(usdt_pairs)}")
        sorted_pairs = sorted(usdt_pairs, key=lambda x: x['volume'], reverse=True)[:50]
        
        return jsonify(sorted_pairs)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
