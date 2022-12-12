from linebot import (LineBotApi)
from linebot.models import *
import user
import settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def pushMessage(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    try:
        Brain = user.UserSay(profile.user_id, event.message.text)
        line_bot_api.push_message(profile.user_id, Brain.process())
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='資訊處理失敗，請稍候再試 Q_Q'))
