from echo import Echo
from realtime import RealTime
from kchart import KChart
from test import MyTest
import re

def UserSay(msg):
    if re.match('s[0-9]{4}', msg.lower()):
        return RealTime(msg)
    elif re.match('k[0-9]{4}', msg.lower()):
        return KChart(msg)
    elif re.match('t[0-9]{4}', msg.lower()):
        return MyTest(msg)
    else:
        return Echo(msg)