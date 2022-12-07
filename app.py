from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from module import *
from home import *

app = Flask(__name__)

line_bot_api = LineBotApi('PkZbi8GG6shNjSE2XFuGwUSGnq47syMHGIm+d+jTmyARlldwnK2AgK6bGsq5j+5Ip6vaqDLcW2Hmkf3RkPptwcV0XIvQv8pFP8AYcseOpIOgCKOUT4lZLAp5Qlyf8UuBTAjcobSElNshbNk/+CBG5gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2e51efac60ec2bcef3cd8a9c9b849796')

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id

    Bot = UserSay(event.message.text)
    returnMessage = Bot.process()
    line_bot_api.push_message(uid, returnMessage)

    return 0

@app.route('/')
def index():
    return processIndex()

if __name__ == '__main__':
   app.run()
