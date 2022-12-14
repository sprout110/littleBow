from linebot import (LineBotApi)
from linebot.models import *
from model.usersay import UserSay
import conf.settings as settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def replyMessage(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    try:
        Robot = UserSay(profile.user_id, event.message.text)
        line_bot_api.reply_message(event.reply_token, Robot.dosomething())
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('系統忙碌中，請稍候再試 Q_Q'))

def pushMessage(event, msg):
    profile = line_bot_api.get_profile(event.source.user_id)
    try:
        line_bot_api.push_message(profile.user_id, msg)
    except:
        line_bot_api.push_message(profile.user_id, TextSendMessage('系統忙碌中，請稍候再試 Q_Q'))