from model.brain import Brain
from linebot.models import TextSendMessage

class HowTo(Brain):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def thinking(self):
        how = '''輸入s加股票代號，可以看到目前的股價。\n比如s2330。\n\n''' + \
                '''輸入k加股票代號，可以看到k線圖。\n比如k2330。'''
        textSendMessage = TextSendMessage(how)
        return [textSendMessage]