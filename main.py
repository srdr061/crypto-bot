from flask import Flask, jsonify
import requests
from technical_analysis import TechnicalAnalysis

app = Flask(__name__)
ta = TechnicalAnalysis()

@app.route('/technical-analysis')
def get_technical_analysis():
    try:
        # 24 saatlik hacim verilerini al
        ticker_url = 'https://api.binance.com/api/v3/ticker/24hr'
        tickers = requests.get(ticker_url).json()
        
        # USDT çiftlerini hacme göre sırala
        usdt_pairs = [
            t for t in tickers 
            if t['symbol'].endswith('USDT')
        ]
        
        # Hacme göre sırala
        sorted_pairs = sorted(
            usdt_pairs,
            key=lambda x: float(x['volume']),
            reverse=True
        )[:50]
        
        analysis_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_symbol = {
                executor.submit(ta.analyze_all_timeframes, pair['symbol']): pair
                for pair in sorted_pairs
            }
            
            for future in concurrent.futures.as_completed(future_to_symbol):
                pair = future_to_symbol[future]
                base_symbol = pair['symbol'].replace('USDT', '')
                analysis_results[base_symbol] = {
                    'current_price': float(pair['lastPrice']),
                    'volume_24h': float(pair['volume']),
                    'timeframes': future.result()
                }
        
        return jsonify(analysis_results)
    except Exception as e:
        return {"status": "error", "message": str(e)}
