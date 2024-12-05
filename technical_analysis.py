import numpy as np
import talib

class TechnicalAnalysis:
    def __init__(self):
        pass

    def calculate_indicators(self, klines_data):
        close_prices = np.array([float(k[4]) for k in klines_data])
        high_prices = np.array([float(k[2]) for k in klines_data])
        low_prices = np.array([float(k[3]) for k in klines_data])
        
        return {
            'rsi': self.calculate_rsi(close_prices),
            'macd': self.calculate_macd(close_prices),
            'bollinger': self.calculate_bollinger(close_prices)
        }
    
    def calculate_rsi(self, prices):
        rsi = talib.RSI(prices)
        return float(rsi[-1])
    
    def calculate_macd(self, prices):
        macd, signal, hist = talib.MACD(prices)
        return {
            'macd': float(macd[-1]),
            'signal': float(signal[-1]),
            'histogram': float(hist[-1])
        }
    
    def calculate_bollinger(self, prices):
        upper, middle, lower = talib.BBANDS(prices)
        return {
            'upper': float(upper[-1]),
            'middle': float(middle[-1]),
            'lower': float(lower[-1])
        }
