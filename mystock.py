import requests
from bs4 import BeautifulSoup

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
    result = f'{title.get_text()} : {a.get_text()}({s}{b.get_text()})' 
    print(result) #印出結果
    return result