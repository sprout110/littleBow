from userspeak import UserSpeak
from linebot.models import ImageSendMessage
import mplfinance as mpf
import yfinance as yf
import pyimgur

IMGUR_CLIENT_ID = 'd82208d3c8f4f9c'

class KChart(UserSpeak):
    def __init__(self, msg):
        super().__init__(msg)
    def process(self):
        content = self.plot_stcok_k_chart(IMGUR_CLIENT_ID, self.msg[1:], '2022-01-01')
        self.result = msg + ' KChart OK' 
        return ImageSendMessage(original_content_url=content, preview_image_url=content)

    def plot_stcok_k_chart(self, IMGUR_CLIENT_ID, stock="0050" , date_from='2020-01-01' ):
        stock = str(stock)+".tw"

        df = yf.download(stock, date_from) 
        mpf.plot(df, type='candle', mav=(5,20), 
                volume=True, 
                ylabel=stock.upper()+' Price' , 
                savefig='testsave.png')
        PATH = "testsave.png"
        im = pyimgur.Imgur(IMGUR_CLIENT_ID)
        uploaded_image = im.upload_image(PATH, title=stock+" candlestick chart")
        return uploaded_image.link