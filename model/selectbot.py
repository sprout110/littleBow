import re
from bots.echo import Echo
from bots.stocknow import StockNow
from bots.howto import HowTo
from bots.showsettings import ShowSettings
from bots.writesettings import WriteSettings
from bots.choicestock import ChoiceStock
from bots.choicekchart import ChoiceKChart
from bots.kchart import KChart
from bots.k10chart import K10Chart
from bots.indices import Indices
from bots.flex01 import Flex01
from bots.readdbfavorite import ReadDBFavorite
from bots.insertfavorite import InsertFavorite
from bots.deletefavorite import DeleteFavorite
from bots.adjustfavorite import AdjustFavorite
from bots.choiceaddstock import ChoiceAddStock

def SelectBot(uid, msg):
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
    elif 'Flex01' == msg:
        return Flex01(uid, msg)
    elif re.match('^[0-9]{4}$', msg):
        return WriteSettings(uid, msg)
    elif re.match('^新增[0-9]{4}$', msg):
        return InsertFavorite(uid, msg)
    elif re.match('^刪除[0-9]{4}$', msg):
        return DeleteFavorite(uid, msg)
    elif re.match('^＠更新選股',msg):
        return ReadDBFavorite(uid, msg)
    elif re.match('^＠增刪選股',msg):
        return AdjustFavorite(uid, msg)
    elif re.match('^＠新增選股',msg):
        print('here')
        return ChoiceAddStock(uid, msg)
    else:
        return Echo(uid, msg)

