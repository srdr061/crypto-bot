from flask import Flask, jsonify
import requests
from technical_analysis import TechnicalAnalysis
import concurrent.futures

app = Flask(__name__)
ta = TechnicalAnalysis()

@app.route('/top-coins')
def get_top_coins():
    try:
        ticker_url = 'https://api.binance.com/api/v3/ticker/24hr'
        tickers = requests.get(ticker_url).json()
        
        usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
        sorted_pairs = sorted(
            usdt_pairs,
            key=lambda x: float(x['volume']),
            reverse=True
        )[:50]
        
        return jsonify({
            'coins': [{'symbol': p['symbol'], 'volume': p['volume']} for p in sorted_pairs]
        })
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/analysis/<symbol>')
def get_single_analysis(symbol):
    try:
        analysis = ta.analyze_all_timeframes(symbol)
        return jsonify(analysis)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/batch-analysis/<int:start>/<int:end>')
def get_batch_analysis(start, end):
    try:
        coins = requests.get(f"{request.host_url}top-coins").json()['coins']
        batch_coins = coins[start:end]
        
        analysis_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_symbol = {
                executor.submit(ta.analyze_all_timeframes, coin['symbol']): coin
                for coin in batch_coins
            }
            
            for future in concurrent.futures.as_completed(future_to_symbol):
                coin = future_to_symbol[future]
                base_symbol = coin['symbol'].replace('USDT', '')
                analysis_results[base_symbol] = future.result()
        
        return jsonify(analysis_results)
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
