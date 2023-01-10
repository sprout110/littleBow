from model.basebot import Basebot
from linebot.models import TextSendMessage

class HowTo(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def Process(self):
        how = '''輸入s加股票代號，可以看到目前的股價。\n比如s2330。\n\n''' + \
               '''輸入k加股票代號，可以看到k線圖。\n比如k2330。'''
        return [TextSendMessage('早盤交易時間 09:00 - 13:30'),
                TextSendMessage('盤後交易時間 14:00 - 14:30'),
                TextSendMessage('盤中零股時間 09:00 - 13:30'),
                TextSendMessage('盤後零股時間 13:40 - 14:30'),
                TextSendMessage(how)]