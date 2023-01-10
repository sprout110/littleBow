import pandas as pd
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
            else:
                self.updateStock(stock, filepath)

            return [TextSendMessage('目前選擇的股票為：' + self.msg)]
        except:
            return [TextSendMessage('設定失敗')]

    def saveStock(self, stock, filepath):
        if not os.path.isfile(filepath):
            stock = stock +".tw"
            taiwan_stock = yf.download(stock, start = '2000-1-1')
            taiwan_stock.to_csv(filepath)
            mydb.has_update_stockhist(stock)

    def updateStock(self, stock, filepath):
        if os.path.isfile(filepath) and not mydb.is_update_stockhist(stock):
            data = pd.read_csv(filepath,  header=0, index_col=0)
            data.index = pd.to_datetime(data.index)
            startDate = data.iloc[-1].name.date()
            dfYahoo = yf.download(stock +".tw", start = startDate)
            if dfYahoo.shape[0]>0:
                pd.concat([data.iloc[:-1], dfYahoo]).to_csv(filepath)
                mydb.has_update_stockhist(stock)
# testWriteSettings = WriteSettings('uid','2413')
# testWriteSettings.dosomething()

