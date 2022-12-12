from botbrain import BotBrain
from echo import Echo
from stock import Stock
from kchart import KChart
from test import MyTest
import re

def UserSay(uid, msg):
    if re.match('s[0-9]{4}', msg.lower()):
        return Stock(uid, msg)
    elif re.match('k[0-9]{4}', msg.lower()):
        return KChart(uid, msg)
    elif re.match('t[0-9]{4}', msg.lower()):
        return MyTest(uid, msg)
    elif 'i love you' == msg.lower():
        return BotBrain(uid, msg)
    else:
        return Echo(uid, msg)


'''
echo1 = Echo("echo", "I love you.")
stock1 = Stock("stock", "s2412")
kchart1 = KChart("kchart", "k2412")
test1 = MyTest('test', 't2412')

print(echo1.thinking())
print(stock1.thinking())
print(kchart1.thinking())
print(test1.thinking())
'''
