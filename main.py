from flask import Flask, jsonify
import requests
from technical_analysis import TechnicalAnalysis

app = Flask(__name__)
ta = TechnicalAnalysis()

@app.route('/technical-analysis')
def get_technical_analysis():
    try:
        symbols = requests.get('https://data-api.binance.vision/api/v3/ticker/price').json()
        analysis_results = {}
        
        for symbol in symbols:
            if symbol['symbol'].endswith('USDT'):
                klines = requests.get(
                    'https://data-api.binance.vision/api/v3/klines',
                    params={
                        'symbol': symbol['symbol'],
                        'interval': '4h',
                        'limit': 100
                    }
                ).json()
                
                base_symbol = symbol['symbol'].replace('USDT', '')
                analysis_results[base_symbol] = {
                    'current_price': float(symbol['price']),
                    'indicators': ta.calculate_indicators(klines)
                }
        
        return jsonify(analysis_results)
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
