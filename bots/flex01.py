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

                        # reply = FlexSendMessage(
            #     alt_text='hello',
            #     contents={
            #         "type": "bubble",
            #         "hero": {
            #             "type": "image",
            #             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
            #             "size": "full",
            #             "aspectRatio": "20:13",
            #             "aspectMode": "cover",
            #             "action": {
            #             "type": "uri",
            #             "uri": "http://linecorp.com/"
            #             }
            #         },
            #         "body": {
            #             "type": "box",
            #             "layout": "vertical",
            #             "contents": [{
            #                     "type": "text",
            #                     "text": "Brown Cafe",
            #                     "weight": "bold",
            #                     "size": "xl"
            #             }]
            #         }
            #     })

            return [message]


            reply = TemplateSendMessage(
                alt_text = 'Buttons template',
                template = ButtonsTemplate(
                    title='Menu',
                    text = '請選擇股票:',
                    actions=[
                        MessageTemplateAction(
                            label='中華食',
                            text='新增4205'                        
                        ),
                        MessageTemplateAction(
                            label='中碳',
                            text='新增1723'
                        ),
                        MessageTemplateAction(
                            label='統一超',
                            text='新增2912'
                        ),
                        MessageTemplateAction(
                            label='精華',
                            text='新增1565'
                        ),
                        # MessageTemplateAction(
                        #     label='大豐電',
                        #     text='新增6184'
                        # )
                    ]
                )
            )

        except:
            textSendMessage = TextSendMessage('發生錯誤: ' + self.msg)
            self.result = 'Send "' + self.msg + 'Fail'
            return [textSendMessage]