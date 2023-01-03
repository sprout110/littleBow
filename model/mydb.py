import pymongo
import certifi
#import urllib.parse
import datetime
from cachetools import Cache

#================================== mongo db =================================
DBName = 'howard-good31'
ClName = 'mystock'

def constructor():
    client = pymongo.MongoClient("mongodb+srv://sprout110:3ljigrgL@cluster0.g1hys5s.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client.test
    db = client[DBName]
    return db

def write_user_stock_fountion(uid, stock, bs, price):  
    db=constructor()
    collect = db[ClName]
    collect.insert_one({
                    "uid": uid,
                    "stock": stock,
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })

def delete_user_stock_fountion(uid):  
    db=constructor()
    collect = db[ClName]
    collect.delete_many({"uid": uid})
    #coll.delete_one({'username':'ketio'})

def read_user_stock_function(uid):
    db = constructor()
    collect = db[ClName]
    cel = list(collect.find({"uid": uid}))
    return cel

def update_user_stock_function(uid, stock, bs, price):
    db = constructor()
    collect = db[ClName]
    collect.update_one({"uid":uid}, 
                       {"$set":   {"stock":stock,
                                   "bs": bs,
                                   "price": float(price),
                                   "date_info": datetime.datetime.utcnow()
                                   }})

#========================================= Cache ================================

cache = Cache(maxsize=100)

def delete_user_setting(uid):
    cache[uid] = None

defaultFavorite = [
            {
                'stock' : '2330',
                'stockName' : '台積電'
            }, {
                'stock' : '2412',
                'stockName' : '中華電'
            }, {
                'stock' : '2002',
                'stockName' : '中鋼'
            }, {
                'stock' : '0050',
                'stockName' : '台灣50'
            }, {
                'stock' : '1737',
                'stockName' : '臺鹽'
            }, {
                'stock' : '1216',
                'stockName' : '統一'
            }, {
                'stock' : '2891',
                'stockName' : '中信金'
            }
        ]

def write_user_setting(uid, stock, favorite = defaultFavorite):
    cache[uid] = {
        'stock' : stock, 
        'favorite' : favorite
    }  

def update_user_setting(uid, stock, favorite = defaultFavorite):
    cache[uid] = {
        'stock' : stock, 
        'favorite' : favorite
    }

def read_user_setting(uid):
    try:
        cel = [{
            'uid' : uid, 
            'stock' : cache[uid]['stock'],
            'favorite' : cache[uid]['favorite']
        }]
    except:
        cel = [{
            "uid" : uid, 
            "stock" : '2412',
            'favorite' : defaultFavorite
        }]
    
    return cel


cache2 = Cache(maxsize=1600)
def has_update_stockhist(stock):
    cache2[stock] = {
        'date' : datetime.datetime.today().strftime('%Y-%m-%d')
    }

def is_update_stockhist(stock):
    try:
        if cache2[stock]['date'] == datetime.datetime.today().strftime('%Y-%m-%d'):
            return True
        else:
            return False 
    except:
        return False



