from userspeak import UserSpeak
from linebot.models import ImageSendMessage
import mplfinance as mpf
import yfinance as yf
import pyimgur
import datetime

IMGUR_CLIENT_ID = 'd82208d3c8f4f9c'

class MyTest(UserSpeak):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)
        startTime = ''
        endTime = ''

    def process(self, startTime = '2020-01-01'):
        self.startTime = startTime
        stock = str(self.msg[1:5])+".tw"
        imgUrl = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , self.startTime)
        self.result = stock + ' KChart OK ' + imgUrl

        return [ImageSendMessage(original_content_url = imgUrl, preview_image_url = imgUrl)]

    def plot_stcok_k_chart(self, IMGUR_CLIENT_ID, stock = "0050" , startTime = '2020-01-01'):
        df = yf.download(stock, start = startTime) 

        tempImgFile = self.uid + ".png"

        mpf.plot(df, 
                type='candle', 
                mav=(5,20), 
                volume = True, 
                ylabel = stock.upper()+' Price' , 
                savefig = tempImgFile)

        im = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = im.upload_image(tempImgFile, title = stock + " candlestick chart")

        return uploaded_image.link

# y = datetime.date.today().year
# m = datetime.date.today().month
# d = datetime.date.today().day
# print(y)
# print(m)
# print(d)

# print(datetime.date(y-10, 1, 1))
# print(datetime.date(y-2, 1, 1))
# print(datetime.date(y, m-2, 1))
