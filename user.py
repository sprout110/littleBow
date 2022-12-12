from echo import Echo
from realtime import RealTime
from kchart import KChart
from test import MyTest
import re

def UserSay(uid, msg):
    if re.match('s[0-9]{4}', msg.lower()):
        return RealTime(uid, msg)
    elif re.match('k[0-9]{4}', msg.lower()):
        return KChart(uid, msg)
    elif re.match('t[0-9]{4}', msg.lower()):
        return MyTest(uid, msg)
    else:
        return Echo(uid, msg)