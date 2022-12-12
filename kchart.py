from linebot.models import ImageSendMessage
import matplotlib
matplotlib.use('Agg')
import mplfinance as mpf
import yfinance as yf
import pyimgur
import datetime

from userspeak import UserSpeak

IMGUR_CLIENT_ID = 'd82208d3c8f4f9c'

class KChart(UserSpeak):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
        startTime = ''
        endTime = ''

    def process(self, startTime = '2020-01-01'):
        self.startTime = startTime
        stock = str(self.msg[1:5])+".tw"
        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day

        #imgUrl1 = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , datetime.date(y-3, 1, 1), 'line', (5, 20), '1')
        imgUrl2 = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, stock , datetime.date(y, m-2, 1), 'candle', (5, 20), '2')
        #self.result = stock + ' KChart OK imgUrl1 ' + imgUrl1 + ', imgUrl2 ' + imgUrl2
        self.result = 'success'

        #return [ImageSendMessage(original_content_url = imgUrl1, preview_image_url = imgUrl1),
        return [ImageSendMessage(original_content_url = imgUrl2, preview_image_url = imgUrl2)]

    def plot_stcok_k_chart(self, IMGUR_CLIENT_ID, stock, startTime, myType = 'candle', myMav = (5, 20), serial = '0'):
        df = yf.download(stock, start = startTime) 
        tempFile = self.uid + serial + '.png'
        mpf.plot(df, 
                type = myType, 
                mav = myMav, 
                volume = True, 
                ylabel = stock.upper() + ' ' + str(myMav) , 
                savefig = tempFile)

        im = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = im.upload_image(tempFile, title = stock + " candlestick chart")

        return uploaded_image.link
