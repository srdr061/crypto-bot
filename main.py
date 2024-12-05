from flask import Flask, jsonify
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

def get_klines(symbol, interval, limit=1):
    url = f'https://data-api.binance.vision/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    return response.json()

@app.route('/usdt-analysis')
def get_usdt_analysis():
    try:
        # Tüm fiyatları al
        price_url = 'https://data-api.binance.vision/api/v3/ticker/price'
        price_data = requests.get(price_url).json()
        
        # Sonuçları topla
        analysis = {}
        intervals = {
            '15m': '15m',
            '1h': '1h',
            '4h': '4h',
            '1d': '1d'
        }
        
        for coin in price_data:
            if coin['symbol'].endswith('USDT'):
                symbol = coin['symbol']
                base_symbol = symbol.replace('USDT', '')
                
                analysis[base_symbol] = {
                    'current_price': float(coin['price']),
                    'changes': {}
                }
                
                # Her interval için değişimi hesapla
                for interval_name, interval_code in intervals.items():
                    kline = get_klines(symbol, interval_code)[0]
                    open_price = float(kline[1])
                    close_price = float(kline[4])
                    change = ((close_price - open_price) / open_price) * 100
                    
                    analysis[base_symbol]['changes'][interval_name] = {
                        'change_percent': round(change, 2),
                        'volume': float(kline[5])
                    }
                
        return jsonify(analysis)
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
