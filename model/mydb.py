import pymongo
import certifi
#import urllib.parse
import datetime
from cachetools import Cache
import model.getdata as getdata

#================================== mongo db =================================
DBName = 'howard-good31'
ClectionName = 'mystock'
Favorite = 'myfavorite'

def constructor():
    client = pymongo.MongoClient("mongodb+srv://sprout110:3ljigrgL@cluster0.g1hys5s.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client[DBName]
    return db

def write_user_stock_fountion(uid, stock, bs, price):  
    db=constructor()
    collect = db[ClectionName]
    collect.insert_one({
                    "uid": uid,
                    "stock": stock,
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })

def delete_user_stock_fountion(uid):  
    db=constructor()
    collect = db[ClectionName]
    collect.delete_many({"uid": uid})
    #coll.delete_one({'username':'ketio'})

def read_user_stock_function(uid):
    db = constructor()
    collect = db[ClectionName]
    cel = list(collect.find({"uid": uid}))
    return cel

def update_user_stock_function(uid, stock, bs, price):
    db = constructor()
    collect = db[ClectionName]
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
                'stock' : '0050',
                'stockName' : '台灣50'
            }, {
                'stock' : '2412',
                'stockName' : '中華電'
            }, {
                'stock' : '1737',
                'stockName' : '臺鹽'
            }, {
                'stock' : '1216',
                'stockName' : '統一'
            }, {
                'stock' : '2891',
                'stockName' : '中信金'
            }, {
                'stock' : '2812',
                'stockName' : '台中銀'
            }
        ]

# db=constructor()
# collect = db[Favorite]
# collect.insert_one({"uid": 'Uf005f1db11566194e221f598c3f0cb92',"stock": '0050', "updateTime": datetime.datetime.utcnow() })
# collect.insert_one({"uid": 'Uf005f1db11566194e221f598c3f0cb92',"stock": '2412', "updateTime": datetime.datetime.utcnow() })
# collect.insert_one({"uid": 'Uf005f1db11566194e221f598c3f0cb92',"stock": '1737', "updateTime": datetime.datetime.utcnow() })
# collect.insert_one({"uid": 'Uf005f1db11566194e221f598c3f0cb92',"stock": '1216', "updateTime": datetime.datetime.utcnow() })
# collect.insert_one({"uid": 'Uf005f1db11566194e221f598c3f0cb92',"stock": '2812', "updateTime": datetime.datetime.utcnow() })
# collect.insert_one({"uid": 'Uf005f1db11566194e221f598c3f0cb92',"stock": '2891', "updateTime": datetime.datetime.utcnow() })

def insert_user_setting(uid, stock):
    cache[uid] = {
        'stock' : stock
    }

def update_user_setting(uid, stock):
    cache[uid]['stock'] = stock

def read_user_setting(uid):
    readDB = False
    #uid = uid + 'test'
    try:
        cache[uid]
    except:
        readDB = True

    if readDB:
        try:
            myFavorites = readFavoriteFromDB(uid)
            #print(myFavorites)
            if len(myFavorites) == 0:
                cache[uid] = {
                    'stock' : '2412', 
                    'favorite' : defaultFavorite
                }
                for item in defaultFavorite:
                    insertFavorite(uid, item['stock'])
            else:    
                cache[uid] = {
                    'stock' : '2412', 
                    'favorite' : myFavorites
                }
        except:
            cache[uid] = {
                'stock' : '2412', 
                'favorite' : defaultFavorite
            }
      
    settings = [{
        'uid' : uid, 
        'stock' : cache[uid]['stock'],
        'favorite' : cache[uid]['favorite']
    }]

    return settings

def read_user_favorites_fromdb(uid):
    myFavorites = readFavoriteFromDB(uid)

    cache[uid] = {
        'stock' : cache[uid]['stock'], 
        'favorite' : myFavorites
    }

def insertFavorite(uid, stock):
    db=constructor()
    collect = db[Favorite]
    collect.insert_one({
        "uid": uid,
        "stock": stock, 
        "updateTime": datetime.datetime.utcnow() 
    })

def removeFavorit(uid, stock):
    db=constructor()
    collect = db[Favorite]
    collect.delete_many({'uid':uid, 'stock':stock})

def readFavoriteFromDB(uid):
    db = constructor()
    collect = db[Favorite]
    myFavorites = list(collect.find({"uid": uid}))
    myFavoritesDict = {}
    for item in myFavorites:
        try:
            myFavoritesDict[item['stock']] = { 
                'stock':item['stock'],
                'stockName': getdata.getStockInfo(item['stock'])['stockName'].iloc[0]
            }
        except:
            print("An exception occurred")

    return myFavoritesDict.values()

# 判斷今日是否已更新 csv 檔
cache2 = Cache(maxsize=1600)
def has_update_stockhist(stock):
    cache2[stock] = {
        'date': datetime.datetime.today().strftime('%Y-%m-%d')
    }

def is_update_stockhist(stock):
    try:
        if cache2[stock]['date'] == datetime.datetime.today().strftime('%Y-%m-%d'):
            return True
        else:
            return False 
    except:
        return False


# db=constructor()
# collect = db[Favorite]
# collect.delete_many({'uid':'Uf005f1db11566194e221f598c3f0cb92', 'stock':'4205'})
