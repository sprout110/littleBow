from model.brain import BaseBrain
from linebot.models import TextSendMessage
import model.mydb as mydb

class UserSettings(BaseBrain):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def thinking(self):
        list = mydb.read_user_setting(self.uid)
        if len(list) == 0:
            mydb.write_user_setting(self.uid, '2412')
            list = [{'uid':self.uid, 'stock':'2412'}]
        text = '目前選擇的股票為：' + list[0]['stock'] #+ '\n'
        #text += '其它：'

        return [TextSendMessage(text)]


#test = MyTest('testUid', 't2412')
#print(test.process())
