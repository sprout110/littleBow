from model.basebot import Basebot
from linebot.models import TextSendMessage
import model.mydb as mydb

class ReadDBFavorite(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def Process(self):
        mydb.read_user_favorites_fromdb(self.uid)
        return [TextSendMessage('OK')]