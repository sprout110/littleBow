from userspeak import UserSpeak
from linebot.models import TextSendMessage

class RealTime(UserSpeak):
    def __init__(self, msg):
        super().__init__(msg)
    def process(self):
        self.result = self.msg[1:] + ' RealTime OK' 
        return TextSendMessage(self.result)



