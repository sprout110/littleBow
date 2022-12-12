import pymongo
import certifi
#import urllib.parse
import datetime

Authdb='howard-good31'

def constructor():
    client = pymongo.MongoClient("mongodb+srv://sprout110:3ljigrgL@cluster0.g1hys5s.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client.test
    db = client[Authdb]
    return db

def write_user_stock_fountion(uid, stock, bs, price):  
    db=constructor()
    collect = db['mystock']
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
    collect = db['mystock']
    collect.delete_many({"uid": uid, "stock": stock})
    #coll.delete_one({'username':'ketio'})

def show_user_stock_fountion(uid):  
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"uid": uid}))
    
    return cel
