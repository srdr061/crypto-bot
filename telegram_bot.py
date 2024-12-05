from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import matplotlib.pyplot as plt
import mplfinance as mpf

class TelegramBot:
    def __init__(self):
        self.token = "7783024050:AAGa6SOPgUpzi-qRAFFDSuFZGrqFPluD4BU"
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.setup_handlers()

    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("analyze", self.analyze_coin))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.handle_message))

    def start(self, update, context):
        update.message.reply_text('Merhaba! Coin analizi için /analyze COINADI komutunu kullanın.')

    def analyze_coin(self, update, context):
        if len(context.args) < 1:
            update.message.reply_text('Lütfen coin adı girin. Örnek: /analyze BTC')
            return

        symbol = context.args[0].upper() + 'USDT'
        self.send_analysis(update, symbol)

    def send_analysis(self, update, symbol):
        # Veri toplama
        dc = DataCollector()
        df = dc.get_historical_data(symbol, '4h')
        df = dc.add_indicators(df)

        # Grafik oluşturma
        self.create_chart(df, symbol)
        
        # Analiz mesajı
        analysis = self.generate_analysis(df, symbol)
        
        # Grafik ve mesaj gönderme
        update.message.reply_photo(open('chart.png', 'rb'))
        update.message.reply_text(analysis)

    def create_chart(self, df, symbol):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Mum grafiği
        mpf.plot(df, type='candle', style='charles',
                title=f'{symbol} Analysis',
                ylabel='Price',
                ax=ax1)
        
        # İndikatörler
        ax2.plot(df.index, df['RSI'], label='RSI')
        ax2.axhline(y=70, color='r', linestyle='--')
        ax2.axhline(y=30, color='g', linestyle='--')
        
        plt.savefig('chart.png')
        plt.close()
