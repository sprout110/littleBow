from model.basebot import Basebot
from linebot.models import TextSendMessage
import model.mydb as mydb

class InsertFavorite(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def Process(self):
        stock = self.msg[2:6]
        print(stock)
        mydb.insertFavorite(self.uid, stock)
        return [TextSendMessage('OK')]