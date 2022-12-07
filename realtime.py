from userspeak import UserSpeak
from linebot.models import TextSendMessage

class RealTime(UserSpeak):
    def __init__(self, msg):
        super().__init__(msg)

    def process(self):
        stock = str(self.msg[1:5]) + ".tw"
        self.result = stock + ' RealTime OK' 
        return TextSendMessage(self.result)



