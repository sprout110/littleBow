#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('PkZbi8GG6shNjSE2XFuGwUSGnq47syMHGIm+d+jTmyARlldwnK2AgK6bGsq5j+5Ip6vaqDLcW2Hmkf3RkPptwcV0XIvQv8pFP8AYcseOpIOgCKOUT4lZLAp5Qlyf8UuBTAjcobSElNshbNk/+CBG5gdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('2e51efac60ec2bcef3cd8a9c9b849796')

#line_bot_api.push_message('1657687512', TextSendMessage(text='你可以開始了'))

@app.route('/')
def index():
    return "<p>Hello World!</p>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)
    
if __name__ == "__main__": #如果以主程式運行
    app.run() #啟動伺服器