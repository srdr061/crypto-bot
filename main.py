from flask import Flask, jsonify
from binance.client import Client
import os
from datetime import datetime

app = Flask(__name__)
client = Client(None, None, testnet=True)

@app.route('/')
def home():
    return "Binance Service is running!"

@app.route('/coins')
def get_all_coins():
    try:
        # Tüm sembolleri al
        exchange_info = client.get_exchange_info()
        
        # USDT çiftlerini filtrele
        usdt_pairs = [
            symbol['symbol'] for symbol in exchange_info['symbols']
            if symbol['symbol'].endswith('USDT') and symbol['status'] == 'TRADING'
        ]
        
        # Her coin için detaylı bilgi
        coin_details = []
        for pair in usdt_pairs:
            ticker = client.get_ticker(symbol=pair)
            coin_details.append({
                'symbol': pair,
                'price': ticker['lastPrice'],
                'change_24h': ticker['priceChangePercent'],
                'volume': ticker['volume'],
                'timestamp': datetime.now().isoformat()
            })
            
        return jsonify(coin_details)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
