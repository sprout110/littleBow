from linebot.models import (ImageSendMessage, TextSendMessage)
import matplotlib as mpl
import numpy as np
import matplotlib.font_manager as font_manager
zhfont = font_manager.FontProperties(fname="NotoSansTC-Light.otf")
font_manager.fontManager.addfont("NotoSansTC-Light.otf")
import mplfinance as mpf
import datetime
from model.basebot import Basebot
import model.getdata as getdata
import model.getimg as getimg

class KChart(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)

    def dosomething(self, test = False):
        msglist = self.msg.split()

        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day

        tempFile = ''

        try:
            if len(msglist) == 1:
                stock = str(self.msg[1:5])
                startDate = datetime.datetime(y-1, m, 1)
                endDate = datetime.datetime(y,m,d) + datetime.timedelta(days=1)
                tempFile = self.plot_stcok_k_chart(stock , startDate, endDate, 'line', test)

            elif len(msglist) == 2:
                stock = str(msglist[0][1:5])
                startDate = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
                endDate = datetime.datetime(y,m,d) + datetime.timedelta(days=1)
                #if (datetime.datetime.now() - datetime.datetime.strptime(msglist[1], '%Y-%m-%d')).total_seconds() < 60*60*24*130:
                if datetime.datetime.strptime(msglist[1], '%Y-%m-%d') >= datetime.datetime(y + ((m-3)//12), (m-3) % 12, 1):
                    tempFile = self.plot_stcok_k_chart(stock , startDate, endDate, 'candle', test)
                else:
                    tempFile = self.plot_stcok_k_chart(stock , startDate, endDate, 'line', test)
                
                if test == True:
                    mpf.show()

            elif len(msglist) == 3:
                stock = str(msglist[0][1:5])
                startDate = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
                endDate = datetime.datetime.strptime(msglist[2], '%Y-%m-%d') + datetime.timedelta(days=1)
                #print(endDate)
                tempFile = self.plot_stcok_k_chart(stock , startDate, endDate, 'line', test)

            if test == True:
                imgurImg = NullObj
            else:
                imgurImg = getimg.getImgurImg(stock, tempFile)

            self.result = stock + ' KChart OK imgUrl ' + imgurImg.link

            return [ImageSendMessage(original_content_url = imgurImg.link, preview_image_url = imgurImg.link)]
        except:
            return [TextSendMessage("目前尚無資料或系統忙碌中。。。")]

    def plot_stcok_k_chart(self, 
                            stock, 
                            startDate, 
                            endDate,
                            myType = 'candle', 
                            test = False):

        if test == False:
            mpl.use('Agg')

        df = getdata.getData(stock, startDate, endDate)
        last_data = df.iloc[-1]
        last2_data = df.iloc[-2]
        stockInfo = getdata.getStockInfo(stock)

        #MAV
        exp5 = df['Close'].ewm(span=5, adjust=False).mean()
        exp20 = df['Close'].ewm(span=20, adjust=False).mean()
        exp120 = df['Close'].ewm(span=120, adjust=False).mean()
        exp240 = df['Close'].ewm(span=240, adjust=False).mean()

        #MACD
        exp12 = df['Close'].ewm(span=12, adjust=False).mean()
        exp26 = df['Close'].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        histogram[histogram<0] = None
        histogram_positive = histogram
        histogram = macd - signal
        histogram[histogram>0] = None
        histogram_negative = histogram
        
        tempFile = self.uid + '.png'

        fig = mpf.figure(style = myStyle, figsize=(12,8))

        ax1 = fig.add_axes([0.06, 0.35, 0.80, 0.55])
        ax2 = fig.add_axes([0.06, 0.25, 0.80, 0.10], sharex=ax1)
        ax3 = fig.add_axes([0.06, 0.15, 0.80, 0.10], sharex=ax1)
        ax2.set_ylabel('macd')
        ax3.set_ylabel('volume')

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
                mpf.make_addplot(histogram_positive, panel = 1, ylabel='DIF-MACD', type = 'bar', width = 0.7, color = 'red', alpha = 1, secondary_y = False, ax=ax2),
                mpf.make_addplot(histogram_negative, panel = 1, type = 'bar', width = 0.7, color = 'lime', alpha = 1, secondary_y = False, ax = ax2),
                mpf.make_addplot(macd, panel = 1, color = 'red', ylabel = 'MACD', secondary_y = True, linestyle='dashdot', ax = ax2),
                mpf.make_addplot(signal, panel = 1, color = 'lightblue', secondary_y = True, linestyle='dashdot', ax = ax2)
        ]

        kwargs = dict(
                    type = myType,
                    ylabel_lower = 'Volume',
                    datetime_format = '%Y-%m-%d',
                    ylabel = stockInfo['stockName'].iloc[0] +' 股價 週線-紅 月線-橙 半年-黃 年線-綠'
        )

        if stock == '2412' and myType == 'candle':
            kwargs['ylim'] = (104, 126)
            kwargs['xrotation'] = 45
        elif myType == 'candle':
            kwargs['xrotation'] = 45

        mpf.plot(
            df,
            ax = ax1,
            #type = myType
            volume = ax3,
            addplot = apds,
            **kwargs
        )
    
        fig.savefig(tempFile)

        return tempFile


class NullObj:
    link = ''

weekdayDict = {
    '0':'一',
    '1':'二',
    '2':'三',
    '3':'四',
    '4':'五',
    '5':'六',
    '6':'日'
}

def newLabels(df, axes, format):
    newxticks = []
    newlabels = []
    for xt in axes[0].get_xticks():
        p = int(xt)
        if p >= 0 and p < len(df):
            ts = df.index[p]
            newxticks.append(p)
            newlabels.append(ts.strftime(format)+ weekdayDict[str(ts.weekday())])

    newxticks.append(len(df)-1)
    newlabels.append(df.index[len(df)-1].strftime(format)+ weekdayDict[str(df.index[len(df)-1].weekday())])

    axes[0].set_xticks(newxticks)
    axes[0].set_xticklabels(newlabels)

def newLabels2(df, ax1, format):
    newxticks = []
    newlabels = []
    for xt in ax1.get_xticks():
        p = int(xt)
        if p >= 0 and p < len(df):
            ts = df.index[p]
            newxticks.append(p)
            newlabels.append(ts.strftime(format)+ weekdayDict[str(ts.weekday())])

    newxticks.append(len(df)-1)
    newlabels.append(df.index[len(df)-1].strftime(format)+ weekdayDict[str(df.index[len(df)-1].weekday())])

    ax1.set_xticks(newxticks)
    ax1.set_xticklabels(newlabels)

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

#['zhfont1', 'SimHei', 'Microsoft JhengHei', 'AR PL UMing CN'],

title_font = {
    'fontname': zhfont.get_name(), 
              'size':     '16',
              'color':    'black',
              'weight':   'bold',
              'va':       'bottom',
              'ha':       'center'}

large_red_font = {
    'fontname': 'Arial',
                  'size':     '24',
                  'color':    'red',
                  'weight':   'bold',
                  'va':       'bottom'}

large_green_font = {
    'fontname': 'Arial',
                    'size':     '24',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}

small_red_font = {
    'fontname': 'Arial',
                  'size':     '11',
                  'color':    'red',
                  'weight':   'bold'
}

small_green_font = {
    'fontname': 'Arial',
                    'size':     '12',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}

normal_label_font = {
    'fontname': zhfont.get_name(),
                     'size':     '12',
                     'color':    'black',
                     'va':       'bottom',
                     'ha':       'right'}
normal_font = {
    'fontname': 'Arial',
               'size':     '12',
               'color':    'black',
               'va':       'bottom',
               'ha':       'left'}

# testKchart = KChart('uid','k2412 2022-9-1')
# testKchart.dosomething(test = True)