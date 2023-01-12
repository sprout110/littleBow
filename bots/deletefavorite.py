from model.basebot import Basebot
from linebot.models import TextSendMessage
import model.mydb as mydb

class DeleteFavorite(Basebot):
    def __init__(self, uid, msg):
        super().__init__(uid, msg)
    def Process(self):
        stock = self.msg[2:6]
        mydb.removeFavorit(self.uid, stock)
        return [TextSendMessage('OK')]