from linebot.models import (ImageSendMessage)
import matplotlib as mpl
import numpy as np
import matplotlib.font_manager as font_manager
font_manager.fontManager.addfont("NotoSansTC-Light.otf")
zhfont = font_manager.FontProperties(fname="NotoSansTC-Light.otf")
import mplfinance as mpf
import datetime
from model.basebot import Basebot
import model.getdata as getdata
import model.getimg as getimg
import os

class K10Chart(Basebot):
    def __init__(self, uid, msg, test = False):
        super().__init__(uid, msg)
        self.test = test

    def dosomething(self):
        msglist = self.msg.split()

        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day

        if len(msglist) == 2:
            stock = str(msglist[0][3:7])
            startDate = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
            endDate = datetime.datetime(y, m, d) + datetime.timedelta(seconds=-1)
        
            figName = stock + startDate.strftime("-%Y%m%d") + endDate.strftime("-%Y%m%d") + ".png"
            if self.test == True:
                self.plot_stcok_k10_chart(stock , startDate, endDate, figName)
                mpf.show()
            else:
                mpl.use('Agg')
                if not os.path.exists(figName):
                    self.plot_stcok_k10_chart(stock , startDate, endDate, figName)
                imgurImg = getimg.getImgurImg(stock, figName)
                return [ImageSendMessage(original_content_url = imgurImg.link, preview_image_url = imgurImg.link)]
            
            self.result = stock + ' K10Chart OK'
        else:
            stock = str(msglist[0][3:7])
            self.result = stock + ' K10Chart Query String Error!'
            print(self.result)
        
        
    def plot_stcok_k10_chart(self, 
                            stock, 
                            startDate, 
                            endDate,
                            figName = ''):

        df = getdata.getHistData(stock, startDate, endDate)
    
        last_data = df.iloc[-1]
        last2_data = df.iloc[-2]
        stockInfo = getdata.getStockInfo(stock)

        #MAV
        exp5 = df['Close'].ewm(span=5, adjust=False).mean()
        exp20 = df['Close'].ewm(span=20, adjust=False).mean()
        exp120 = df['Close'].ewm(span=120, adjust=False).mean()
        exp240 = df['Close'].ewm(span=240, adjust=False).mean()
        
        myColor = mpf.make_marketcolors(
            up = 'red',
            down = 'limegreen',
            edge = 'black',
            wick = 'inherit',
            volume = 'inherit',
        )

        rc_font = {
            'font.family': zhfont.get_name(),
            'axes.unicode_minus': 'False'
        }

        myStyle = mpf.make_mpf_style(
            marketcolors = myColor,
            figcolor = '#EEEEEE',
            y_on_right = True,
            gridaxis = 'both',
            gridstyle = '-.',
            gridcolor = '#E1E1E1',
            rc = rc_font
        )

        fig = mpf.figure(style = myStyle, figsize=(12,8))
        ax1 = fig.add_axes([0.06, 0.15, 0.80, 0.75])

        fig.text(0.40, 0.96, stock.upper() + '.TW - ' + stockInfo['stockName'].iloc[0])
        
        fig.text(0.08, 0.91, f'{last_data.name.date()}')
        fig.text(0.18, 0.91, '最高: ')
        fig.text(0.21, 0.91, f'{np.round(last_data["High"], 3)}')
        fig.text(0.28, 0.91, '最低: ')
        fig.text(0.31, 0.91, f'{np.round(last_data["Low"], 3)}')
        fig.text(0.38, 0.91, '開盤: ')
        fig.text(0.41, 0.91, f'{np.round(last_data["Open"], 3)}')
        fig.text(0.48, 0.91, '前一日收盤: ')
        fig.text(0.545, 0.91, f'{np.round(last2_data["Close"], 3)}', **small_red_font)
        fig.text(0.60, 0.91, '目前/收盤: ')
        fig.text(0.66, 0.91, f'{np.round(last_data["Close"], 3)}', **small_red_font)
        fig.text(0.72, 0.91, '成交量: ')
        fig.text(0.76, 0.91, f'{np.round(last_data["Volume"]/10000, 3)}' + '萬')

        apds = [
            mpf.make_addplot(exp5  , panel = 0, color='fuchsia',linestyle='dashed' , ax = ax1),
            mpf.make_addplot(exp20 , panel = 0, color='orange' ,linestyle='dashdot', ax = ax1),
            mpf.make_addplot(exp120, panel = 0, color='yellow' ,linestyle='dashdot', ax = ax1),
            mpf.make_addplot(exp240, panel = 0, color='green'  ,linestyle='dashdot', ax = ax1),
        ]

        kwargs = dict(
            type = 'line',
            datetime_format = '%Y-%m-%d',
            ylabel = stockInfo['stockName'].iloc[0] + ' 股價 週線-紅 月線-橙 半年-黃 年線-綠'
        )

        mpf.plot(
            df,
            ax = ax1,
            addplot = apds,
            **kwargs
        )

        fig.savefig(figName)

small_red_font = {
    'fontname': 'Arial',
    'size':     '11',
    'color':    'red',
    'weight':   'bold'
}

# testKchart = K10Chart('uid','k2412 2012-1-1', True)
# testKchart.dosomething()

            