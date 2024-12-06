from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "API is running"

@app.route('/top-coins')
def get_top_coins():
    try:
        # Get price data
        price_url = 'https://data-api.binance.vision/api/v3/ticker/price'
        price_data = requests.get(price_url).json()
        
        # Get 24h volume data
        volume_url = 'https://data-api.binance.vision/api/v3/ticker/24hr'
        volume_data = requests.get(volume_url).json()
        
        # Combine data
        coin_data = {}
        for item in volume_data:
            if item['symbol'].endswith('USDT'):
                coin_data[item['symbol']] = {
                    'symbol': item['symbol'],
                    'volume': float(item['volume']),
                    'price': 0
                }
                
        # Add price data
        for item in price_data:
            if item['symbol'] in coin_data:
                coin_data[item['symbol']]['price'] = float(item['price'])
        
        # Sort by volume
        sorted_pairs = sorted(
            coin_data.values(), 
            key=lambda x: x['volume'], 
            reverse=True
        )[:50]
        
        return jsonify(sorted_pairs)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
