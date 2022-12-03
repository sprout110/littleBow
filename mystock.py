import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt # 畫圖用
import mplfinance as mpf # 畫蠟燭圖
from pandas_datareader import data
import yfinance as yf
yf.pdr_override()
import pandas as pd
import pyimgur

def get_stock_realtime(stock):
    # 要抓取的網址
    url = 'https://tw.stock.yahoo.com/quote/' + stock 
    #請求網站
    list_req = requests.get(url)
    #將整個網站的程式碼爬下來
    soup = BeautifulSoup(list_req.text, "html.parser")
    title = soup.find('h1', {'class' : 'C($c-link-text)'})			# 找到h1這個標籤
    a = soup.select('.Fz\(32px\)')[0]
    b = soup.select('.Fz\(20px\)')[0]
    s = ''							# 漲或跌的狀態
    try:
        if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C\(\$c-trend-down\)')[0]:
            s = '-'
    except:
        try:
            if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C\(\$c-trend-up\)')[0]:
                s = '+'
        except:
            s = '-'
    result = f'{title.get_text()}{a.get_text()}({s}{b.get_text()})' 
    #print(result) #印出結果
    return result

def plot_stcok_k_chart(IMGUR_CLIENT_ID, stock="0050" , date_from='2020-01-01', date_end='2022-12-01' ):
    """
    進行個股K線繪製，回傳至於雲端圖床的連結。將顯示包含5MA、20MA及量價關係，起始預設自2020-01-01起迄昨日收盤價。
    :stock :個股代碼(字串)，預設0050。
    :date_from :起始日(字串)，格式為YYYY-MM-DD，預設自2020-01-01起。
    """
    stock = str(stock)+".tw"
    # df = web.DataReader(stock, 'yahoo', date_from) 
    df = yf.download(stock, date_from, date_end)
    #mpf.plot(df, type='candle', mav=(5,20), volume=True, ylabel=stock.upper()+' Price')
    mpf.plot(df, type='candle', mav=(5,20), volume=True, ylabel=stock.upper()+' Price' , savefig='testsave.png')
    PATH = "testsave.png"
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=stock+" candlestick chart")
    return uploaded_image.link

# Client ID:d82208d3c8f4f9c
# Client secret:cdc03db440e9d286f5cda8af3ec033d25726956f

def plot_stock_k_chart(IMGUR_CLIENT_ID, stock="0050" , start_date='2020-01-01', end_date='2022-12-01'):
    data = yf.download(str(stock)+".tw", start_date, end_date)
    print(data)
    color=mpf.make_marketcolors(up='red', down='green', inherit=True)
    style=mpf.make_mpf_style(base_mpf_style='default', rc=font, marketcolors=color)
    
    mpf.plot(data=data, type='candle', style=style, volume=True, title=str(stock)+".tw", tight_layout=True, mav=(5,20), figratio=(16, 9), figscale=0.5) # 繪製 5, 20 日收盤價均線

    PATH = "k_chart.png"
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=stock+" candlestick chart")
    return uploaded_image.link

plot_stock_k_chart('d82208d3c8f4f9c', '2412', '2022-01-01', '2022-12-03')
#plot_stcok_k_chart('d82208d3c8f4f9c', '2412', '2022-01-01', '2022-12-03')

    
