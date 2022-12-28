from linebot.models import (ImageSendMessage, TextSendMessage)
import matplotlib as mpl
import numpy as np
from matplotlib.font_manager import FontProperties as font
zhfont = font(fname="NotoSansTC-Light.otf")
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
font_manager.fontManager.addfont("NotoSansTC-Light.otf")
plt.rcParams['font.sans-serif'] = [zhfont.get_name()]
plt.rcParams['axes.unicode_minus'] = False
import mplfinance as mpf
import datetime
from model.basebot import Basebot
from conf import settings
import model.getdata as getdata
import model.getimg as getimg

IMGUR_CLIENT_ID = settings.IMGUR_CLIENT_ID

class KChart(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)

    def dosomething(self, test = False):
        msglist = self.msg.split()
        if len(msglist) == 1:
            stock = str(self.msg[1:5])
            y = datetime.date.today().year
            m = datetime.date.today().month
            d = datetime.date.today().day
            imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , datetime.date(y-3, m, 1), datetime.datetime.today(), 'line', '2', test)
        elif len(msglist) == 2:
            stock = str(msglist[0][1:5])
            startTime = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
            if (datetime.datetime.now() - datetime.datetime.strptime(msglist[1], '%Y-%m-%d')).total_seconds() < 11000000:
                imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, datetime.datetime.today(), 'candle', '1', test)
            else:    
                imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, datetime.datetime.today(), 'line', '1', test)
        elif len(msglist) == 3:
            stock = str(msglist[0][1:5])
            startTime = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
            endTime = datetime.datetime.strptime(msglist[2], '%Y-%m-%d')
            imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, endTime, 'line', '1', test)

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
                            endTime,
                            myType = 'candle', 
                            serial = '0',
                            test = False):

        if test == False:
            mpl.use('Agg')

        df = getdata.getData(stock, startTime, endTime)
        last_data = df.iloc[-1]
        last2_data = df.iloc[-2]
        dfStockInfo = getdata.getStockInfo(stock)

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
        
        kwargs = dict(
                    type = myType,
                    #volume = True,
                    #title = '\n\n' + stock.upper() + '.TW - ' + dfStockInfo['stockName'].iloc[0],
                    ylabel_lower = 'Volume',
                    datetime_format = '%Y-%m-%d',
                    ylabel = dfStockInfo['stockName'].iloc[0] +' 股價 週線-紅 月線-橙 半年-黃 年線-綠'
        )

        if stock == '2412' and myType == 'candle':
            kwargs['ylim'] = (104, 126)
            kwargs['xrotation'] = 45
        elif myType == 'candle':
            kwargs['xrotation'] = 45

        tempFile = self.uid + serial + '.png'

        fig = mpf.figure(style = myStyle, figsize=(12,8))

        ax1 = fig.add_axes([0.06, 0.35, 0.80, 0.55])
        ax2 = fig.add_axes([0.06, 0.25, 0.80, 0.10], sharex=ax1)
        ax3 = fig.add_axes([0.06, 0.15, 0.80, 0.10], sharex=ax1)

        #ax1.set_ylabel('price2 週-紅 月-橙 半年-黃 年-綠')
        ax2.set_ylabel('macd')
        ax3.set_ylabel('volume')

        t1 = fig.text(0.40, 0.96, stock.upper() + '.TW - ' + dfStockInfo['stockName'].iloc[0])
        t2 = fig.text(0.40, 0.91, '開盤: ')
        t3 = fig.text(0.43, 0.91, f'{np.round(last_data["Open"], 3)}')
        t4 = fig.text(0.50, 0.91, '目前/收盤: ')
        t5 = fig.text(0.56, 0.91, f'{np.round(last_data["Close"], 3)}')
        t6 = fig.text(0.20, 0.91, '最高: ')
        t7 = fig.text(0.23, 0.91, f'{np.round(last_data["High"], 3)}')
        t8 = fig.text(0.30, 0.91, '最低: ')
        t9 = fig.text(0.33, 0.91, f'{np.round(last_data["Low"], 3)}')
        #print(df.tail(5))
        t10 = fig.text(0.60, 0.91, '前日收盤: ')
        t11 = fig.text(0.65, 0.91, f'{np.round(last2_data["Close"], 3)}')
        t12 = fig.text(0.70, 0.91, '成交量: ')
        t13 = fig.text(0.74, 0.91, f'{np.round(last_data["Volume"]/10000, 3)}' + '萬')
        t14 = fig.text(0.08, 0.91, f'{last_data.name.date()}')
        #print(last_data)
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

        # fig, axes = mpf.plot(
        #         data = df,
        #         addplot = apds, 
        #         **kwargs,
        #         num_panels = 3,
        #         main_panel = 0,
        #         volume_panel = 2,
        #         style = myStyle,
        #         figratio=(7,5),
        #         #savefig = tempFile,
        #         #hlines=dict(hlines=[12,4], linewidths=(2,3.5)),
        #         tight_layout = False,
        #         returnfig=True)

        # if myType == 'candle':
        #     ##format = '%Y-%b-%d'
        #     ##format = '%Y-%m-%d'
        #     #format = '%b-%d'
        #     format = '%m/%d'
        #     newLabels(df, axes, format)
        # else:
        #     format = '%Y-%m-%d'
        #     newLabels(df, axes, format)

        if myType == 'candle':
            ##format = '%Y-%b-%d'
            ##format = '%Y-%m-%d'
            #format = '%b-%d'
            format = '%m/%d'
            #newLabels2(df, ax3, format)
        else:
            format = '%Y-%m-%d'
            #newLabels2(df, ax3, format)

        mpf.plot(
            df,
            ax = ax1,
            #type = myType
            volume = ax3,
            addplot = apds,
            **kwargs
        )
    
        if test == True:
            mpf.show()
            #fig.savefig(tempFile)
            imgurImg = NullObj
        else:
            fig.savefig(tempFile)
            imgurImg = getimg.getImgurImg(stock, tempFile)

        return imgurImg.link


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

# NotoSansTC-Light.otf
# MicrosoftJhengHeiLight-01.ttf
# zhfont = mpl.font_manager.FontProperties(fname='NotoSansTC-Light.otf').get_name()
# print(zhfont)
rc_font = {
     'font.family': zhfont.get_name(), #'Microsoft JhengHei',
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
    'fontname': 'Microsoft JhengHei', 
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
                  'size':     '12',
                  'color':    'red',
                  'weight':   'bold',
                  'va':       'bottom'}

small_green_font = {
    'fontname': 'Arial',
                    'size':     '12',
                    'color':    'green',
                    'weight':   'bold',
                    'va':       'bottom'}

normal_label_font = {
    'fontname': 'Microsoft JhengHei',
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

#testKchart = KChart('uid','k2412 2012-1-1 2014-1-1')
#testKchart.dosomething(test = True)