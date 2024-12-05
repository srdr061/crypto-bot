from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Binance Service is running!"

@app.route('/all-coins')
def get_all_coins():
    try:
        url = 'https://data-api.binance.vision/api/v3/ticker/price'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        
        usdt_pairs = []
        for coin in data:
            if coin['symbol'].endswith('USDT'):
                usdt_pairs.append({
                    'symbol': coin['symbol'],
                    'price': float(coin['price'])
                })
        return jsonify(usdt_pairs)  # Tüm USDT çiftlerini döndür
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
