from model.basebot import Basebot
from linebot.models import (TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction)
import model.mydb as mydb

class ChoiceStock(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def Process(self):
        try:
            userSetting = mydb.read_user_setting(self.uid)
            # print(userSetting[0])
            # print(userSetting[0]['favorite'])
            items = []
            for item in userSetting[0]['favorite']:
                # print(item)
                items.append(QuickReplyButton(
                            action = MessageAction(item['stockName'],item['stock']),
                        ))

            # print(items)

            reply = TextSendMessage(
                text = '請選擇股票：',
                quick_reply= QuickReply(
                    items = items
                )
            )

            return [reply]
        except:
            return [TextSendMessage('發生錯誤')]