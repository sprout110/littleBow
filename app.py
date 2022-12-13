from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
import pages.home as home 
import model.dialog as dialog
import config.settings as settings

app = Flask(__name__)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
#line_bot_api.push_message(settings.LINE_USER_ID, TextSendMessage(text='你可以開始了'))

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
    dialog.replyMessage(event)
    return 0

if __name__ == '__main__':
   app.run()
