import yfinance as yf
from linebot.models import TextSendMessage
from model.basebot import Basebot
import model.mydb as mydb
import model.getdata as getdata
import datetime
import os

class WriteSettings(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def dosomething(self):
        try:
            stock = self.msg
            settings = mydb.read_user_setting(self.uid)
            filepath = r'k' + str(stock) + '.tw.csv'

            #print(settings)
            if len(settings) > 1:
                mydb.delete_user_setting(self.uid)
                mydb.insert_user_setting(self.uid, stock)
            elif len(settings) == 1:
                mydb.update_user_setting(self.uid, stock)
            elif len(settings) == 0:
                mydb.insert_user_setting(self.uid, stock)

            if not os.path.isfile(filepath):
                self.saveStock(stock, filepath)

            return [TextSendMessage('目前選擇的股票為：' + self.msg)]
        except:
            return [TextSendMessage('設定失敗')]

    def saveStock(self, stock, filepath):
        stock = stock +".tw"
        taiwan_stock = yf.download(stock, start = '2002-1-1')
        taiwan_stock.to_csv(filepath)

# testWriteSettings = WriteSettings('uid','2413')
# testWriteSettings.dosomething()

