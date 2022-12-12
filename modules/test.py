from model.brain import Brain
from linebot.models import TextSendMessage
import model.mongodb as mongodb

class MyTest(Brain):
    def __init__(self, uid,  msg):
        super().__init__(uid, msg)

    def process(self):
        mongodb.write_user_stock_fountion(uid = 'uid', stock='2412', bs='>', price='25')

        return [TextSendMessage('2412已經儲存成功')]


#test = MyTest('testUid', 't2412')
#print(test.process())

 
# y = datetime.date.today().year
# m = datetime.date.today().month
# d = datetime.date.today().day
# print(y)
# print(m)
# print(d)

# print(datetime.date(y-10, 1, 1))
# print(datetime.date(y-2, 1, 1))
# print(datetime.date(y, m-2, 1))
