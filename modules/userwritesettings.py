from model.brain import BaseBrain
from linebot.models import TextSendMessage
import model.mongodb as mongodb

class UserWriteSettings(BaseBrain):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def thinking(self):
        try:
            list = mongodb.read_user_setting(self.uid)
            print(list)
            if len(list) > 1:
                mongodb.delete_user_setting(self.uid)
                mongodb.write_user_setting(self.uid, self.msg)
            elif len(list) == 1:
                mongodb.update_user_setting(self.uid, self.msg)
            elif len(list) == 0:
                mongodb.write_user_setting(self.uid, self.msg)

            return [TextSendMessage('設定成功')]
        except:
            return [TextSendMessage('設定失敗')]