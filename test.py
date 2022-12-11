from userspeak import UserSpeak
from linebot.models import ImageSendMessage
import mplfinance as mpf
import yfinance as yf
import pyimgur
import datetime
import mongodb

IMGUR_CLIENT_ID = 'd82208d3c8f4f9c'

class MyTest(UserSpeak):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)
        startTime = ''
        endTime = ''

    def process(self):
        mongodb.write_user_stock_fountion(stock='2412', bs='>', price='25')

        return ['2412已經儲存成功']

 
# y = datetime.date.today().year
# m = datetime.date.today().month
# d = datetime.date.today().day
# print(y)
# print(m)
# print(d)

# print(datetime.date(y-10, 1, 1))
# print(datetime.date(y-2, 1, 1))
# print(datetime.date(y, m-2, 1))
