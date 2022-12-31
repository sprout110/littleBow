import yfinance as yf
from linebot.models import TextSendMessage
from model.basebot import Basebot
import model.mydb as mydb
import model.getdata as getdata
import datetime

class WriteSettings(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def dosomething(self):
        try:
            list = mydb.read_user_setting(self.uid)
            if len(list) > 1:
                mydb.delete_user_setting(self.uid)
                mydb.write_user_setting(self.uid, self.msg)
            elif len(list) == 1:
                mydb.update_user_setting(self.uid, self.msg)
            elif len(list) == 0:
                mydb.write_user_setting(self.uid, self.msg)

            stock = self.msg
            #print(stock)
            try:
                y = datetime.date.today().year
                m = datetime.date.today().month
                d = datetime.date.today().day
                df = getdata.getHistData(stock, startDate=str(y) + '-1-1', endDate=str(y) + '-2-1')
            except:
                stock = stock +".tw"
                taiwan_stock = yf.download(stock, start = '2012-1-1')
                taiwan_stock.to_csv('data/k' + str(stock) + '.csv')

            return [TextSendMessage('目前選擇的股票為：' + self.msg)]
        except:
            return [TextSendMessage('設定失敗')]

# testWriteSettings = WriteSettings('uid','2413')
# testWriteSettings.dosomething()

