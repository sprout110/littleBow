from model.basebot import Basebot
from linebot.models import (TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction)
import datetime
import model.mydb as mydb

class ChoiceKChart(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def dosomething(self):
        try:
            y = datetime.date.today().year
            m = datetime.date.today().month
            d = datetime.date.today().day
            dataList = mydb.read_user_setting(self.uid)
            if len(dataList) == 0:
                mydb.write_user_setting(self.uid, '2412')
                dataList = [{'uid':self.uid, 'stock':'2412'}]

            items = [
                        QuickReplyButton(
                            action = MessageAction('三個月', 
                            'k' + dataList[0]['stock'] + ' ' + str(y) + '-' + str(m-3) + '-1')
                        ),
                        QuickReplyButton(
                            action= MessageAction('一年', 
                            'k' + dataList[0]['stock'] + ' ' + str(y-1) + '-' + str(m) + '-1')
                        ),
                        QuickReplyButton(
                            action= MessageAction('十年', 
                            'k10' + dataList[0]['stock'] + ' ' + str(y-10) + '-' + str(m) + '-1')
                        )
                    ]

            for item in range(y-1, y-10, -1):
                # print(item)
                startDate = str(item) + '-1-1'
                endDate = str(item+1) + '-1-1'
                items.append(QuickReplyButton(
                            action = MessageAction(str(item),
                            'k' + dataList[0]['stock'] + ' ' + startDate + ' ' + endDate)
                        ))

            reply = TextSendMessage(
                text = '請選擇時間：',
                quick_reply= QuickReply(
                    items = items
                )
            )

            return [reply]
        except:
            return [TextSendMessage('發生錯誤')]