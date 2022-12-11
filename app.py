from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from mylinebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage)
from module import *
import home
import mylinebot

import settings

app = Flask(__name__)

handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@app.route('/')
def index():
    return home.home()

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

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    mylinebot.sendMessage(event)
    return 0

if __name__ == '__main__':
   app.run()
