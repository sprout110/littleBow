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

class Indices(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)

    def Process(self):
        msglist = self.msg.split()
        indices = msglist[0]
        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day
        startTime = datetime.date(y-3, m, 1)

        if len(msglist) >= 1:
            startTime = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')

        imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, indices , startTime, 'line', '1')
        self.result = indices + ' KChart OK imgUrl ' + imgUrl

        return [ImageSendMessage(original_content_url = imgUrl, preview_image_url = imgUrl)]

    def plot_stcok_k_chart(self, 
                            IMGUR_CLIENT_ID, 
                            stock, 
                            startTime, 
                            myType = 'candle', 
                            serial = '0'):

        df = yf.download(stock, start = startTime)

        #MACD
        exp5 = df['Close'].ewm(span=5, adjust=False).mean()
        exp20 = df['Close'].ewm(span=20, adjust=False).mean()
        exp120 = df['Close'].ewm(span=120, adjust=False).mean()
        exp240 = df['Close'].ewm(span=240, adjust=False).mean()
        #print(exp240.head(10))
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
        
        apds = [mpf.make_addplot(exp5, panel =0,color='red',linestyle='dashdot'),
                mpf.make_addplot(exp20, panel=0, color='orange',linestyle='dashdot'),
                mpf.make_addplot(histogram, panel = 1, type = 'bar', width = 0.7, color = 'dimgray', alpha = 1, secondary_y = False),
                mpf.make_addplot(macd, panel = 1, color = 'red', ylabel = 'MACD', secondary_y = True),
                mpf.make_addplot(signal, panel = 1, color = 'orange', secondary_y = True,linestyle='dashdot')
                ]
        kwargs = dict(type = myType,
                    volume = True,
                    title = '\n\n' + stock.upper(),
                    ylabel_lower = 'Volume')

        if stock == '2412.tw' and myType == 'candle':
            apds.append(mpf.make_addplot(exp240, panel=0, color='yellow',linestyle='dashdot'))
            apds.append(mpf.make_addplot(exp240, panel=0, color='yellow',linestyle='dashdot'))
            #     mpf.make_addplot(exp12, panel=0,color='c',linestyle='dashdot'),
            #     mpf.make_addplot(exp26, panel=0,color='lime',linestyle='dashdot')])
            kwargs['ylabel'] = stock.upper() + ' mav(5, 20, 120, 240)'
            kwargs['ylim'] = (104,120)
            kwargs['datetime_format'] ='%m/%d'
            kwargs['xrotation'] = 0
        elif myType == 'candle':
            apds.append([mpf.make_addplot(exp240, panel=0, color='yellow',linestyle='dashdot')])
            kwargs['ylabel'] = stock.upper() + ' mav(5, 20, 240)'
            kwargs['datetime_format'] ='%m/%d'
            kwargs['xrotation'] = 0
        else:
            apds.append([mpf.make_addplot(exp240, panel=0, color='yellow',linestyle='dashdot')])
            kwargs['ylabel'] = stock.upper() + ' mav(5, 20, 240)'
            kwargs['datetime_format'] = '%Y-%m-%d'

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