from model.basebot import Basebot
from linebot.models import (FlexSendMessage, MessageTemplateAction, DatetimePickerAction, LocationAction, URIAction, TemplateSendMessage, ButtonsTemplate, TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction)
import model.mydb as mydb

class ChoiceAddStock(Basebot):
    def __init__(self, uid,  msg):
        ().__init__(uid, msg)

    def Process(self):
        try:
            reply = FlexSendMessage(
                alt_text='hi',
                contents={
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "選單",
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": "請選擇股票",
                            "size": "md",
                            "color": "#9C9C9C"
                        }
                        ],
                        "action": {
                        "type": "message",
                        "label": "action",
                        "text": "default"
                        }
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "中華食",
                                "text": "新增4205"
                            }
                        },{
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "中碳",
                                "text": "新增1723"
                            }
                        },{
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "統一超",
                                "text": "新增2912"
                            }
                        },{
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "精華",
                                "text": "新增1565"
                            }
                        },{
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "大豐電",
                                "text": "新增6184"
                            }
                        }
                        ]
                    },
                    "styles": {
                        "footer": {
                        "separator": True
                        }
                    }
                }
            )

            return [reply]
        except:
            return [TextSendMessage('發生錯誤')]