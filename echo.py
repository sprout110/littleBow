from botbrain import BotBrain
from linebot.models import TextSendMessage

class Echo(BotBrain):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def thinking(self):
        textSendMessage = TextSendMessage('You say: ' + self.msg)
        self.result = 'Send "' + self.msg + '" OK'
        return [textSendMessage]