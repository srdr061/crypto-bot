from flask import Flask, jsonify
from data_collector import DataCollector
from pattern_recognition import PatternRecognition
from news_analyzer import NewsAnalyzer
from telegram_bot import TelegramBot
import schedule
import time
import threading

app = Flask(__name__)
dc = DataCollector()
pr = PatternRecognition()
na = NewsAnalyzer()
bot = TelegramBot()

def analyze_markets():
    try:
        # Tüm USDT çiftlerini al
        pairs = dc.get_all_pairs()
        
        for pair in pairs:
            # Veri topla
            df = dc.get_historical_data(pair, '4h')
            df = dc.add_indicators(df)
            
            # Formasyonları kontrol et
            patterns = pr.detect_patterns(df)
            
            # Haberleri analiz et
            news_sentiment = na.analyze_sentiment(pair)
            
            # Sinyal kontrolü
            if check_signals(df, patterns, news_sentiment):
                signal_message = generate_signal_message(pair, df, patterns, news_sentiment)
                bot.send_signal(signal_message)
                
    except Exception as e:
        print(f"Error in market analysis: {str(e)}")

def check_signals(df, patterns, sentiment):
    # Sinyal mantığı
    return True if (
        df['RSI'].iloc[-1] < 30 or 
        df['RSI'].iloc[-1] > 70 or 
        any(patterns.values())
    ) else False

# Periyodik analiz
schedule.every(15).minutes.do(analyze_markets)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule thread'ini başlat
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    
    # Flask uygulamasını başlat
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
