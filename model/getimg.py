import pyimgur
from conf import settings

IMGUR_CLIENT_ID = settings.IMGUR_CLIENT_ID

def getImgurImg(stock, tempFile):
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    return im.upload_image(tempFile, title = stock + " chart")