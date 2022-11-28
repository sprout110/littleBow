# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pymongo
import certifi
import urllib.parse
import datetime
###############################################################################
#                       股票機器人 Python基礎教學 【pymongo教學】                      #
###############################################################################

# Authentication Database認證資料庫
Authdb='howard-good31'

##### 資料庫連接 #####
def constructor():
    #client = MongoClient('你的連接指令')
    client = pymongo.MongoClient("mongodb+srv://sprout110:3ljigrgL@cluster0.g1hys5s.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
    db = client.test
    db = client[Authdb]
    return db
   
#----------------------------儲存使用者的股票--------------------------
def write_user_stock_fountion(stock, bs, price):  
    db=constructor()
    collect = db['mystock']
    collect.insert_one({"stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.utcnow()
                    })
    
#----------------------------殺掉使用者的股票--------------------------
def delete_user_stock_fountion(stock):  
    db=constructor()
    collect = db['mystock']
    collect.delete_many({"stock": stock})
    #coll.delete_one({'username':'ketio'})
    
#----------------------------秀出使用者的股票--------------------------
def show_user_stock_fountion():  
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"data": 'care_stock'}))

    return cel



