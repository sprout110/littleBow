import pymongo
import certifi
#import urllib.parse
import datetime

DBName = 'howard-good31'
CollectionName = 'mystock'

def constructor():
    client = pymongo.MongoClient("mongodb+srv://sprout110:3ljigrgL@cluster0.g1hys5s.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client.test
    db = client[DBName]
    return db

def write_user_stock_fountion(uid, stock, bs, price):  
    db=constructor()
    collect = db[CollectionName]
    collect.insert_one({
                    "uid": uid,
                    "stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })

def delete_user_stock_fountion(uid, stock):  
    db=constructor()
    collect = db[CollectionName]
    collect.delete_many({"uid": uid, "stock": stock})
    #coll.delete_one({'username':'ketio'})

def delete_user_setting(uid):
    db=constructor()
    collect = db[CollectionName]
    collect.delete_many({"uid": uid})

def write_user_setting(uid, stock):
    db = constructor()
    collect = db[CollectionName]
    collect.insert_one({"uid":uid, 
                        "stock":stock,
                        "date_info": datetime.datetime.utcnow()
                        })

def update_user_setting(uid, stock):
    db = constructor()
    collect = db[CollectionName]
    collect.update_one(
                {"uid":uid}, 
                {
                    "$set": {"uid":uid, "stock":stock}
                }) 

def read_user_setting(uid):  
    db = constructor()
    collect = db['mystock']
    cel = list(collect.find({"uid": uid}))
    
    return cel
