import talib
import numpy as np

class PatternRecognition:
    def __init__(self):
        self.patterns = {
            'Doji': talib.CDLDOJI,
            'Engulfing': talib.CDLENGULFING,
            'Hammer': talib.CDLHAMMER,
            'Morning Star': talib.CDLMORNINGSTAR,
            'Evening Star': talib.CDLEVENINGSTAR
        }

    def detect_patterns(self, df):
        pattern_results = {}
        for pattern_name, pattern_func in self.patterns.items():
            pattern_results[pattern_name] = pattern_func(
                df['open'].values,
                df['high'].values,
                df['low'].values,
                df['close'].values
            )
        return pattern_results
