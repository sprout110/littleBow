from linebot import (LineBotApi)
from linebot.models import *
import model.usersay as usersay
import config.settings as settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def replyMessage(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    try:
        Brain = usersay.UserSay(profile.user_id, event.message.text)
        #line_bot_api.push_message(profile.user_id, Brain.thinking())
        line_bot_api.reply_message(event.reply_token, Brain.thinking())
    except:
        #line_bot_api.push_message(profile.user_id, TextSendMessage(text='系統忙碌中，請稍候再試 Q_Q'))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='系統忙碌中，請稍候再試 Q_Q'))
