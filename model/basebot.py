from linebot.models import TextSendMessage
class Basebot:

    def __init__(self, uid, msg):
        self.uid = uid
        self.msg = msg
        self.result = ''

    def Process(self):
        self.result = '使用者代號 "' + str(self.uid) + '" 說 "' + self.msg + '"'
        return TextSendMessage('Hello, World!')


""" 
Brain = BotBrain("botbrain", "i love you")
result = Brain.thinking()
print(result) 
"""
