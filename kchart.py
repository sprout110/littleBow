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
            if (datetime.datetime.now() - datetime.datetime.strptime(msglist[1], '%Y-%m-%d')).total_seconds() < 11000000:
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

        #MACD
        exp5 = df['Close'].ewm(span=5, adjust=False).mean()
        exp20 = df['Close'].ewm(span=20, adjust=False).mean()

        exp12 = df['Close'].ewm(span=12, adjust=False).mean()
        exp26 = df['Close'].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        exp12 = df['Close'].ewm(span=12, adjust=False).mean()
        exp26 = df['Close'].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        
        
        if stock == '2412.tw' and myType == 'candle':
            apds = [mpf.make_addplot(exp5, panel =0,color='red',linestyle='dashdot'),
                mpf.make_addplot(exp20, panel=0,color='orange',linestyle='dashdot'),
                mpf.make_addplot(exp12, panel=0,color='c',linestyle='dashdot'),
                mpf.make_addplot(exp26, panel=0,color='lime',linestyle='dashdot'),
                mpf.make_addplot(histogram, panel = 1, type = 'bar', width = 0.7, color = 'dimgray', alpha = 1, secondary_y = False),
                mpf.make_addplot(macd, panel = 1, color = 'red', ylabel = 'MACD', secondary_y = True),
                mpf.make_addplot(signal, panel = 1, color = 'orange', secondary_y = True)
                ]
            kwargs = dict(
                type = myType,
                volume = True,
                title = '\n\n' + stock.upper(),
                ylabel = stock.upper() + ' MAV(5, 12, 20, 26)',
                ylabel_lower = 'Volume',
                #figratio=(1200/72,480/60),
                #figscale=3,
                datetime_format='%m/%d',
                xrotation = 0,
                ylim = (104,120)
            )
        elif myType == 'candle':
            apds = [mpf.make_addplot(exp5, panel =0,color='red'),
                mpf.make_addplot(exp20, panel=0,color='orange'),
                mpf.make_addplot(exp12, panel=0,color='c',linestyle='dashdot'),
                mpf.make_addplot(exp26, panel=0,color='lime',linestyle='dashdot'),
                mpf.make_addplot(histogram, panel = 1, type = 'bar', width = 0.7, color = 'dimgray', alpha = 1, secondary_y = False),
                mpf.make_addplot(macd, panel = 1, color = 'red', ylabel = 'MACD', secondary_y = True),
                mpf.make_addplot(signal, panel = 1, color = 'orange', secondary_y = True)]
            kwargs = dict(
                type = myType,
                volume = True,
                title = '\n\n' + stock.upper(),
                ylabel = stock.upper() + ' MAV(5, 12, 20, 26)',
                ylabel_lower = 'Volume',
                #figratio=(1200/72,480/60),
                #figscale=3,
                datetime_format='%m/%d',
                xrotation = 0
            )
        else:
            apds = [mpf.make_addplot(exp5, panel =0,color='red'),
                mpf.make_addplot(exp20, panel=0,color='orange'),
                mpf.make_addplot(histogram, panel = 1, type = 'bar', width = 0.7, color = 'dimgray', alpha = 1, secondary_y = False),
                mpf.make_addplot(macd, panel = 1, color = 'red', ylabel = 'MACD', secondary_y = True),
                mpf.make_addplot(signal, panel = 1, color = 'orange', secondary_y = True)]
            kwargs = dict(
                type = myType,
                volume = True,
                title = '\n\n' + stock.upper(),
                ylabel = stock.upper() + ' MAV(5, 12, 20, 26)',
                ylabel_lower = 'Volume',
                datetime_format='%Y-%m-%d'
            )


        tempFile = self.uid + serial + '.png'
        mpf.plot(df, 
                **kwargs,
                addplot = apds,
                num_panels = 3,
                main_panel = 0,
                volume_panel = 2,
                style = my_style,
                savefig = tempFile)

        im = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = im.upload_image(tempFile, title = stock + " candlestick chart")

        return uploaded_image.link


my_color = mpf.make_marketcolors(
    up = 'red',
    down = 'limegreen',
    edge = 'inherit',
    wick = 'inherit',
    volume = 'inherit',
)

my_style = mpf.make_mpf_style(
    marketcolors = my_color,
    figcolor='#EEEEEE',
    y_on_right = True,
    gridaxis='both',
    gridstyle='-.',
    gridcolor='#E1E1E1',
    #rc={'font.family':'Microsoft JhengHei'}
)