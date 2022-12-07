from userspeak import UserSpeak
from linebot.models import TextSendMessage

class Echo(UserSpeak):
    def __init__(self, msg):
        super().__init__(msg)
    def process(self):
        textSendMessage = TextSendMessage(self.msg)
        self.result = 'Send "' + self.msg + '" OK'
        return [textSendMessage]