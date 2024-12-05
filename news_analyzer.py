import requests
from textblob import TextBlob
import pandas as pd

class NewsAnalyzer:
    def __init__(self):
        self.news_api_key = "YOUR_NEWS_API_KEY"
        self.news_endpoint = "https://cryptonews-api.com/api/v1"

    def get_crypto_news(self, symbol):
        params = {
            'tickers': symbol,
            'items': 50,
            'token': self.news_api_key
        }
        response = requests.get(self.news_endpoint, params=params)
        return response.json()

    def analyze_sentiment(self, news_data):
        sentiments = []
        for news in news_data['data']:
            analysis = TextBlob(news['title'])
            sentiments.append(analysis.sentiment.polarity)
        return np.mean(sentiments)
