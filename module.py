from echo import Echo
from realtime import RealTime
from kchart import KChart

def UserSay(msg):
    if msg == 's2412':
        return RealTime(msg)
    elif msg == 'k2412':
        return KChart(msg)
    else:
        return Echo(msg)