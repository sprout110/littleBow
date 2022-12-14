from model.brain import BaseBrain
from linebot.models import TextSendMessage

class Echo(BaseBrain):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def thinking(self):
        textSendMessage = TextSendMessage('You say: ' + self.msg)
        self.result = 'Send "' + self.msg + '" OK'
        return [textSendMessage]