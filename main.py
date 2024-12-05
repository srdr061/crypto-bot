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
        # Binance API'den sembol fiyatlarını al
        response = requests.get('https://api.binance.com/api/v3/ticker/price')
        if response.status_code == 200:
            data = response.json()
            # Sadece USDT çiftlerini filtrele
            usdt_pairs = []
            for coin in data:
                if isinstance(coin, dict) and coin['symbol'].endswith('USDT'):
                    usdt_pairs.append({
                        'symbol': coin['symbol'],
                        'price': float(coin['price'])
                    })
            # İlk 10 coini döndür
            return jsonify(usdt_pairs[:10])
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
