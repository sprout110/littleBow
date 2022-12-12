import re

from model.brain import Brain
from modules.echo import Echo
from modules.stock import Stock
from modules.test import MyTest
from modules.howto import HowTo
from kchart import KChart

def UserSay(uid, msg):
    if re.match('s[0-9]{4}', msg.lower()):
        return Stock(uid, msg)
    elif re.match('k[0-9]{4}', msg.lower()):
        return KChart(uid, msg)
    elif re.match('t[0-9]{4}', msg.lower()):
        return MyTest(uid, msg)
    elif 'i love you' == msg.strip().lower().strip():
        return Brain(uid, msg)
    elif '@說明'  == msg:
        return HowTo(uid, msg)
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
