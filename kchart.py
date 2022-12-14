from linebot.models import (ImageSendMessage, TextSendMessage)
import matplotlib
matplotlib.use('Agg')
import mplfinance as mpf
import yfinance as yf
import pyimgur
import datetime
from model.basebot import Basebot
from conf import settings
import model.mydb as mydb

IMGUR_CLIENT_ID = settings.IMGUR_CLIENT_ID

class KChart(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)

    def dosomething(self):
        msglist = self.msg.split()
        if len(msglist) == 1: #預設圖為線型，5日，20日均線圖。
            if self.msg == '＠k線圖':
                settinglist = mydb.read_user_setting(self.uid)
                if len(settinglist) == 0:
                    mydb.write_user_setting(self.uid, '2412')
                    settinglist = [{'uid':self.uid, 'stock':'2412'}]
                stock = settinglist[0]['stock']+".tw"
            else:
                stock = str(self.msg[1:5])+".tw"
            
            y = datetime.date.today().year
            m = datetime.date.today().month
            d = datetime.date.today().day
            # print(datetime.date(y-3, m, d))
            imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , datetime.date(y-3, m, 1), 'line', (5, 20), '2')
        else: # ToDo: 若開始和結束時間小於3個月，candle圖，其它為均線圖。
            stock = str(msglist[0][1:5])+".tw"
            startTime = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
            if (datetime.datetime.now() - datetime.datetime.strptime(msglist[1], '%Y-%m-%d')).total_seconds() < 7777000:
                imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, 'candle', (5, 20), '1')
            else:    
                imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, 'line', (5, 20), '1')

        self.result = stock + ' KChart OK imgUrl ' + imgUrl

        return [TextSendMessage('早盤交易時間 09:00 - 13:30'),
                TextSendMessage('盤後交易時間 14:00 - 14:30'),
                TextSendMessage('盤中零股時間 09:00 - 13:30'),
                TextSendMessage('盤後零股時間 13:40 - 14:30'),
                ImageSendMessage(original_content_url = imgUrl, preview_image_url = imgUrl)]

    def plot_stcok_k_chart(self, 
                            IMGUR_CLIENT_ID, 
                            stock, 
                            startTime, 
                            myType = 'candle', 
                            myMav = (5, 20), 
                            serial = '0'):

        df = yf.download(stock, start = startTime)
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
