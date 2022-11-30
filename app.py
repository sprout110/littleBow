# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 01:00:17 2018

@author: linzino
"""


from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import mongodb
import mystock
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
#line_bot_api = LineBotApi('')
# 必須放上自己的Channel Secret
#handler = WebhookHandler('你的Secret')

#line_bot_api.push_message('你的ID', TextSendMessage(text='你可以開始了'))

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('PkZbi8GG6shNjSE2XFuGwUSGnq47syMHGIm+d+jTmyARlldwnK2AgK6bGsq5j+5Ip6vaqDLcW2Hmkf3RkPptwcV0XIvQv8pFP8AYcseOpIOgCKOUT4lZLAp5Qlyf8UuBTAjcobSElNshbNk/+CBG5gdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('2e51efac60ec2bcef3cd8a9c9b849796')

@app.route('/')
def index():
    return "<p>Hello World!</p>"

# 監聽所有來自 /callback 的 Post Request
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
    ### 抓到顧客的資料 ###
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id #使用者ID
    usespeak=str(event.message.text) #使用者講的話
    if re.match('[0-9]{4}[<>][0-9]',usespeak): # 先判斷是否是使用者要用來存股票的
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return 0

    
    elif re.match('刪除[0-9]{4}',usespeak): # 刪除存在資料庫裡面的股票
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0

    elif re.match('s[0-9]{4}',usespeak): #顯示即時股價
        #querystock = mystock.get_stock_realtime(usespeak[1:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[1:]+'即時股價:'))
        return 0

    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token,message)

if __name__ == '__main__':
    app.run(run)