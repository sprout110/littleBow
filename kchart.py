from linebot.models import (ImageSendMessage, TextSendMessage)
import matplotlib
matplotlib.use('Agg')
import mplfinance as mpf
import yfinance as yf
import pyimgur
import datetime
from model.brain import Brain
from config import settings

IMGUR_CLIENT_ID = settings.IMGUR_CLIENT_ID

class KChart(Brain):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)

    def thinking(self):
        list = self.msg.split()
        # print(list)
        if len(list) > 1:
            stock = str(list[0][1:5])+".tw"
            # print(stock)
            endTime = datetime.datetime.strptime(list[1], "%Y-%m-%d")
            # print(endTime)
            imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , endTime, 'line', (5, 15, 60), '1')
        else:
            stock = str(self.msg[1:5])+".tw"
            # print(stock)
            y = datetime.date.today().year
            m = datetime.date.today().month
            d = datetime.date.today().day
            # print(datetime.date(y, m-3, 1))
            imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , datetime.date(y, m-3, 1), 'candle', (5, 8, 20), '2')
        
        self.result = stock + ' KChart OK imgUrl ' + imgUrl

        return [TextSendMessage('早盤交易時間 08:30 - 13:30'),
                TextSendMessage('盤後交易時間 14:00 - 14:30'),
                TextSendMessage('零股交易時間 13:40 - 14:30'),
                ImageSendMessage(original_content_url = imgUrl, preview_image_url = imgUrl)]

    def plot_stcok_k_chart(self, 
                            IMGUR_CLIENT_ID, 
                            stock, 
                            startTime, 
                            myType = 'candle', 
                            myMav = (5, 20), 
                            serial = '0'):

        df = yf.download(stock, start = startTime)
        # print(df) 
        tempFile = self.uid + serial + '.png'
        mpf.plot(df, 
                type = myType, 
                mav = myMav, 
                volume = True, 
                ylabel = stock.upper() + ' ' + str(myMav) , 
                savefig = tempFile)

        im = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = im.upload_image(tempFile, title = stock + " candlestick chart")

        return uploaded_image.link
