from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from module import *
from home import *
import settings

app = Flask(__name__)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

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
    profile = line_bot_api.get_profile(event.source.user_id)

    Bot = UserSay(profile.user_id, event.message.text)
    returnMessage = Bot.process()
    for reply in returnMessage:
        line_bot_api.push_message(profile.user_id, reply)

    return 0

@app.route('/')
def index():
    return processIndex()

if __name__ == '__main__':
   app.run()
