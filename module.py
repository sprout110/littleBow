from echo import Echo
from realtime import RealTime
from kchart import KChart
import re

def UserSay(msg):
    if re.match('s[0-9]{4}', msg):
        return RealTime(msg)
    elif re.match('k[0-9]{4}',msg):
        return KChart(msg)
    else:
        return Echo(msg)