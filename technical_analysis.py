import pandas as pd
import pandas_ta as ta
import requests

class TechnicalAnalysis:
    def __init__(self):
        self.timeframes = {
            '15m': '15m',
            '1h': '1h',
            '4h': '4h',
            '1d': '1d'
        }

    def get_klines(self, symbol, interval, limit=100):
        url = 'https://data-api.binance.vision/api/v3/klines'
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        response = requests.get(url, params=params)
        return response.json()

    def analyze_all_timeframes(self, symbol):
        results = {}
        for tf_name, tf_code in self.timeframes.items():
            klines = self.get_klines(symbol, tf_code)
            results[tf_name] = self.calculate_indicators(klines)
        return results

    def calculate_indicators(self, klines_data):
        df = pd.DataFrame(klines_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_volume', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignored'])
        df = df.astype({'close': 'float', 'high': 'float', 'low': 'float', 'volume': 'float'})

        return {
            'rsi': float(df.ta.rsi().iloc[-1]),
            'macd': self.calculate_macd(df),
            'bollinger': self.calculate_bollinger(df),
            'volume': float(df['volume'].iloc[-1])
        }

    def calculate_macd(self, df):
        macd = df.ta.macd()
        return {
            'macd': float(macd['MACD_12_26_9'].iloc[-1]),
            'signal': float(macd['MACDs_12_26_9'].iloc[-1]),
            'histogram': float(macd['MACDh_12_26_9'].iloc[-1])
        }

    def calculate_bollinger(self, df):
        bb = df.ta.bbands()
        return {
            'upper': float(bb['BBU_20_2.0'].iloc[-1]),
            'middle': float(bb['BBM_20_2.0'].iloc[-1]),
            'lower': float(bb['BBL_20_2.0'].iloc[-1])
        }
