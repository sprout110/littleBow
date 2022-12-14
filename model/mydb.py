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

def write_user_setting(uid, stock):
    cache[uid] = stock

def update_user_setting(uid, stock):
    cache[uid] = stock 

def read_user_setting(uid):
    try:
        cel = [{"uid": uid, "stock":cache[uid]}]
    except:
        print('hi')
        cel = [{"uid": uid, "stock": '2412'}]
    
    return cel
