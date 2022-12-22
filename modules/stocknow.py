from model.basebot import Basebot
from linebot.models import TextSendMessage
import requests
from bs4 import BeautifulSoup
import model.mydb as mydb

class StockNow(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)

    def dosomething(self):
        #stock = str(self.msg[1:5])
        
        try:
            if self.msg == '@目前股價':
                list = mydb.read_user_setting(self.uid)
                stock = list[0]['stock']
            else:
                stock = str(self.msg[1:5])

            reply = self.get_stock_realtime(stock)
            self.result = stock + '.tw RealTime OK'
            return [TextSendMessage(reply)] #, TextSendMessage('輸入k' + stock + '看K線圖')]
        except:
            self.result = '抓取股票：' + stock + '.TW 失敗，沒有股票代號或網站故障。'
            return [TextSendMessage(self.result)]

    def get_stock_realtime(self, stock):
        url = 'https://tw.stock.yahoo.com/quote/' + stock 
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.text, "html.parser")
        title = soup.find('h1', {'class' : 'C($c-link-text)'})
        a = soup.select('.Fz\(32px\)')[0]
        b = soup.select('.Fz\(20px\)')[0]
        s = ''
        try:
            if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C\(\$c-trend-down\)')[0]:
                s = '-'
        except:
            try:
                if soup.select('#main-0-QuoteHeader-Proxy')[0].select('.C\(\$c-trend-up\)')[0]:
                    s = '+'
            except:
                s = '-'
        result = f'{title.get_text()} {a.get_text()}({s}{b.get_text()})' 
        
        return result



