import json
from cachetools import Cache
cacheStock = Cache(maxsize=1600)

def delete_stock(stock, stockName):
    print("")

def write_stock(stock, stockName):
    print("")

def update_stock(stock, stockName):
    print("") 

def read_stock(stock, stockName):
    print("")

def load_stock():
    with open('data.json') as f:
        data = json.load(f)

    for item in data:
        cacheStock[item.stock] = item.stockName

def save_stock():
    if cacheStock.currsize>1:
        with open('output.json', 'w') as f:
            json.dump(cacheStock, f)