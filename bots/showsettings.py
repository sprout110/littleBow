from model.basebot import Basebot
from linebot.models import TextSendMessage
import model.mydb as mydb

class ShowSettings(Basebot):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def Process(self):
        dataList = mydb.read_user_setting(self.uid)
        if len(dataList) == 0:
            mydb.write_user_setting(self.uid, '2412')
            dataList = [{'uid':self.uid, 'stock':'2412'}]
        text = '目前選股為：' + dataList[0]['stock'] #+ '\n'
        #text += '其它：'

        return [TextSendMessage(text)]


#test = MyTest('testUid', 't2412')
#print(test.process())
