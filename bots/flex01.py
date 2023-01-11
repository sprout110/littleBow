from model.basebot import Basebot
from linebot.models import (TextSendMessage, BubbleContainer, 
            FlexSendMessage, BoxComponent,
            TextComponent, ButtonComponent, MessageAction)

class Flex01(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def Process(self):
        try:
            mycontents = []
            for i in range(0, 30):
                mycontents.append(ButtonComponent(
                                    style='primary',
                                    height='sm',
                                    action=MessageAction(label='水泥工業', text='水泥工業')
                        ))
            bubble = BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text='股票名單', size='sm')
                    ]
                ),
                body = BoxComponent(
                     layout='vertical',
                     contents=mycontents
                )
            )
            message = FlexSendMessage(alt_text="彈性配置", contents=bubble)
            return [message]
        except:
            textSendMessage = TextSendMessage('發生錯誤: ' + self.msg)
            self.result = 'Send "' + self.msg + 'Fail'
            return [textSendMessage]