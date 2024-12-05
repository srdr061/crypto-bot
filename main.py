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

@app.route('/usdt')
def get_usdt_pairs():
    try:
        url = 'https://data-api.binance.vision/api/v3/ticker/price'
        response = requests.get(url)
        data = response.json()
        
        # Sadece USDT çiftlerini al ve düzenle
        usdt_pairs = {}
        for coin in data:
            if coin['symbol'].endswith('USDT'):
                symbol = coin['symbol'].replace('USDT', '')
                usdt_pairs[symbol] = float(coin['price'])
                
        return jsonify(usdt_pairs)
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
