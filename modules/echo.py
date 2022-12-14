from model.basebot import Basebot
from linebot.models import TextSendMessage

class Echo(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def dosomething(self):
        textSendMessage = TextSendMessage('You say: ' + self.msg)
        self.result = 'Send "' + self.msg + '" OK'
        return [textSendMessage]