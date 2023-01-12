from model.basebot import Basebot
from linebot.models import (TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction)
import datetime
import model.mydb as mydb

class AdjustFavorite(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def Process(self):
        try:
            items = [
                        QuickReplyButton(
                            action = MessageAction('新增', 
                            '＠新增選股')
                        ),
                        QuickReplyButton(
                            action = MessageAction('刪除', 
                            '＠刪除選股')
                        ),
                        QuickReplyButton(
                            action = MessageAction('更新選股', 
                            '＠更新選股')
                        )
                    ]

            reply = TextSendMessage(
                text = '請選擇：',
                quick_reply= QuickReply(
                    items = items
                )
            )

            return [reply]
        except:
            return [TextSendMessage('發生錯誤')]