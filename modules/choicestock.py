from model.basebot import Basebot
from linebot.models import (TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction)

class ChoiceStock(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def dosomething(self):
        try:
            reply = TextSendMessage(
                text = '請選擇股票：',
                quick_reply= QuickReply(
                    items = [
                        QuickReplyButton(
                            action = MessageAction('台機電','2330'),
                        ),
                        QuickReplyButton(
                            action= MessageAction('中華電','2412')
                        ),
                        QuickReplyButton(
                            action= MessageAction('中鋼', '2002')
                        ),
                        QuickReplyButton(
                            action=MessageAction('元大台灣50','0050')
                        )
                    ]
                )
            )

            return [reply]
        except:
            return [TextSendMessage('發生錯誤')]