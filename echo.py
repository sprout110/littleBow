from userspeak import UserSpeak
from linebot.models import TextSendMessage

class Echo(UserSpeak):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def process(self):
        textSendMessage = TextSendMessage('You(' + self.uid + ') say:' + self.msg)
        self.result = 'Send "' + self.msg + '" OK'
        return [textSendMessage]