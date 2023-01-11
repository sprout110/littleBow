from flask import Flask, render_template, request, abort, redirect, url_for, send_from_directory
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from pages.home import Home 
import model.linebotsay as linebotsay
import conf.settings as settings
import os

app = Flask(__name__)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
#line_bot_api.push_message(settings.LINE_USER_ID, TextSendMessage(text='你可以開始了'))

@app.route('/')
def index():
    return Home()

@app.route('/form1')
def form1():
   return render_template('form1.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    return render_template('hello.html', name = name)

   #if name:
       #print('Request for hello page received with name=%s' % name)
    #return render_template('hello.html', name = name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))

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
    linebotsay.replyMessage(event)
    return 0

if __name__ == '__main__':
   app.run()
