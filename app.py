from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import mongodb
import mystock
import re
from config import * 

app = Flask(__name__)

@app.route('/')
def index():
    return "<p>Hello World!</p>"


if __name__ == '__main__':
    app.run()