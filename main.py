from flask import Flask, jsonify, cache
import requests
import os
from datetime import datetime, timedelta
import concurrent.futures

app = Flask(__name__)

# Cache süresi: 1 dakika
CACHE_DURATION = 60

def fetch_kline_data(symbol, interval):
    url = f'https://data-api.binance.vision/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1
    }
    response = requests.get(url, params=params)
    return symbol, interval, response.json()

@app.route('/usdt-analysis')
def get_usdt_analysis():
    try:
        # Tüm fiyatları al
        price_url = 'https://data-api.binance.vision/api/v3/ticker/price'
        price_data = requests.get(price_url).json()
        
        # Sadece USDT çiftlerini filtrele
        usdt_pairs = [coin for coin in price_data if coin['symbol'].endswith('USDT')]
        
        analysis = {}
        intervals = {'15m': '15m', '1h': '1h', '4h': '4h', '1d': '1d'}
        
        # Paralel veri çekme
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for coin in usdt_pairs[:20]:  # İlk 20 coin için
                symbol = coin['symbol']
                for interval_name, interval_code in intervals.items():
                    futures.append(
                        executor.submit(fetch_kline_data, symbol, interval_code)
                    )
            
            # Sonuçları topla
            for future in concurrent.futures.as_completed(futures):
                symbol, interval, kline_data = future.result()
                base_symbol = symbol.replace('USDT', '')
                
                if base_symbol not in analysis:
                    analysis[base_symbol] = {
                        'current_price': float(next(c['price'] for c in usdt_pairs if c['symbol'] == symbol)),
                        'changes': {}
                    }
                
                kline = kline_data[0]
                open_price = float(kline[1])
                close_price = float(kline[4])
                change = ((close_price - open_price) / open_price) * 100
                
                analysis[base_symbol]['changes'][interval] = {
                    'change_percent': round(change, 2),
                    'volume': float(kline[5])
                }
        
        return jsonify(analysis)
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
