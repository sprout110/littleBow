import re
from modules.echo import Echo
from modules.stocknow import StockNow
from modules.howto import HowTo
from modules.showsettings import ShowSettings
from modules.writesettings import WriteSettings
from modules.choicestock import ChoiceStock
from modules.choicekchart import ChoiceKChart
from kchart import KChart
from k10chart import K10Chart
from indices import Indices

def UserSay(uid, msg):
    #print(msg)
    if re.match('^s[0-9]{4}', msg.lower()):
        return StockNow(uid, msg)
    elif re.match('^k10[0-9]{4}', msg.lower()):
        return K10Chart(uid, msg)
    elif re.match('^k[0-9]{4}', msg.lower()):
        return KChart(uid, msg)
    elif '^TWII' == msg.upper():
        return Indices(uid, msg)
    elif '@說明'  == msg:
        return HowTo(uid, msg)
    elif '@顯示設定' == msg:
        return ShowSettings(uid, msg)
    elif '@選股' == msg:
        return ChoiceStock(uid, msg)
    elif '@目前股價' == msg:
        return StockNow(uid, msg)
    elif '＠k線圖' == msg:
        return ChoiceKChart(uid, msg)
    elif re.match('^[0-9]{4}$', msg):
        return WriteSettings(uid, msg)
    else:
        return Echo(uid, msg)

