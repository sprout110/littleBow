from model.brain import BaseBrain
from linebot.models import TextSendMessage
import model.mydb as mydb

class UserWriteSettings(BaseBrain):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def thinking(self):
        try:
            list = mydb.read_user_setting(self.uid)
            print(list)
            if len(list) > 1:
                mydb.delete_user_setting(self.uid)
                mydb.write_user_setting(self.uid, self.msg)
            elif len(list) == 1:
                mydb.update_user_setting(self.uid, self.msg)
            elif len(list) == 0:
                mydb.write_user_setting(self.uid, self.msg)

            return [TextSendMessage('設定成功')]
        except:
            return [TextSendMessage('設定失敗')]