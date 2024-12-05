from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def home():
    return "Binance Service is running!"

# Test endpoint'i - servisin çalışıp çalışmadığını kontrol eder
@app.route('/test')
def test():
    return {"status": "ok", "message": "Test endpoint working"}

# Tüm USDT çiftlerini getirir
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
        return jsonify(usdt_pairs)
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
