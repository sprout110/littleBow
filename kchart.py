from linebot.models import (ImageSendMessage, TextSendMessage)
import matplotlib as mpl
mpl.use('Agg')
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

    def dosomething(self):
        msglist = self.msg.split()
        if len(msglist) == 1:
            stock = str(self.msg[1:5])
            y = datetime.date.today().year
            m = datetime.date.today().month
            d = datetime.date.today().day
            imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , datetime.date(y-3, m, 1), 'line', '2')
        else: 
            stock = str(msglist[0][1:5])
            startTime = datetime.datetime.strptime(msglist[1], '%Y-%m-%d')
            if (datetime.datetime.now() - datetime.datetime.strptime(msglist[1], '%Y-%m-%d')).total_seconds() < 11000000:
                imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, 'candle', '1')
            else:    
                imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , startTime, 'line', '1')

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
                            serial = '0'):

        df = getdata.getYahooData(stock, startTime)
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
        
        apds = [
                mpf.make_addplot(exp5  , panel = 0, color='fuchsia'    ,linestyle='dashed'),
                mpf.make_addplot(exp20 , panel = 0, color='orange' ,linestyle='dashdot'),
                mpf.make_addplot(exp120, panel = 0, color='yellow' ,linestyle='dashdot'),
                mpf.make_addplot(exp240, panel = 0, color='green'  ,linestyle='dashdot'),
                mpf.make_addplot(histogram_positive, panel = 1, ylabel='DIF-MACD', type = 'bar', width = 0.7, color = 'red', alpha = 1, secondary_y = False),
                mpf.make_addplot(histogram_negative, panel = 1, type = 'bar', width = 0.7, color = 'lime', alpha = 1, secondary_y = False),
                mpf.make_addplot(macd, panel = 1, color = 'red', ylabel = 'MACD', secondary_y = True, linestyle='dashdot'),
                mpf.make_addplot(signal, panel = 1, color = 'lightblue', secondary_y = True, linestyle='dashdot')
        ]

        kwargs = dict(
                    type = myType,
                    volume = True,
                    title = '\n\n' + stock.upper() + '.TW - ' + dfStockInfo['stockName'].iloc[0],
                    ylabel_lower = 'Volume',
                    datetime_format = '%Y-%m-%d',
                    ylabel = 'Price 週-紅 月-橙 半年—黃 年—綠'
        )

        if stock == '2412' and myType == 'candle':
            kwargs['ylim'] = (104, 126)
            kwargs['xrotation'] = 0
        elif myType == 'candle':
            kwargs['xrotation'] = 0

        tempFile = self.uid + serial + '.png'

        fig, axes = mpf.plot(
                data = df,
                addplot = apds, 
                **kwargs,
                num_panels = 3,
                main_panel = 0,
                volume_panel = 2,
                style = my_style,
                figratio=(7,5),
                #savefig = tempFile,
                #hlines=dict(hlines=[12,4], linewidths=(2,3.5)),
                tight_layout = False,
                returnfig=True)

        if myType == 'candle':
            ##format = '%Y-%b-%d'
            ##format = '%Y-%m-%d'
            #format = '%b-%d'
            format = '%m/%d'
            newLabels(df, axes, format)
        else:
            format = '%Y-%m-%d'
            newLabels(df, axes, format)
        
        fig.savefig(tempFile)
        
        imgurImg = getimg.getImgurImg(stock, tempFile)

        return imgurImg.link


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

my_color = mpf.make_marketcolors(
    up = 'red',
    down = 'limegreen',
    edge = 'inherit',
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

my_style = mpf.make_mpf_style(
    marketcolors = my_color,
    figcolor='#EEEEEE',
    y_on_right = True,
    gridaxis='both',
    gridstyle='-.',
    gridcolor='#E1E1E1',
    rc=rc_font
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
