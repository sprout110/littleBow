from model.brain import Brain
from linebot.models import TextSendMessage

class Echo(Brain):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def thinking(self):
        textSendMessage = TextSendMessage('You say: ' + self.msg)
        self.result = 'Send "' + self.msg + '" OK'
        return [textSendMessage]