from linebot import (LineBotApi, WebhookHandler)
from linebot.models import *
from module import UserSay
import settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def pushMessage(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    try:
        Bot = UserSay(profile.user_id, event.message.text)
        returnMessage = Bot.process()
        for reply in returnMessage:
            line_bot_api.push_message(profile.user_id, reply)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='腦子故障中，請稍等再試 Q_Q'))
