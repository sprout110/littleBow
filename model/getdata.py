import pandas as pd
import yfinance as yf
import datetime  as datetime

def getData(stock, startTime):
    df1 = getStockData(stock, startTime)
    df2 = getYahooData(stock, startTime)
    #print(df1.tail(3))
    #print(df2.head(3))
    return pd.concat([df1, df2])

cutDate = '2022-10-01'

def getStockData(stock, startDate='2022-01-01', endDate=cutDate):
    data = pd.read_csv(r'data/k' + stock + '.csv',  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    return data[data.index>startDate][data[data.index>startDate].index<endDate]

def getYahooData(stock, startTime):
    stock = stock +".tw"
    if startTime < datetime.datetime.strptime(cutDate, '%Y-%m-%d'):
        startTime = datetime.datetime.strptime(cutDate, '%Y-%m-%d')
    return yf.download(stock, start = startTime)

def getStockInfo(stock):
    df = pd.read_csv(r'data/stocklist.csv', header=0, index_col='stockId')
    df.index = df.index.map(str)
    #print(type(df.index))
    try:
        data = df[df.index == stock]
        if df[df.index == stock].empty:
            return df[df.index == '0']
        else:
            return df[df.index == stock]
    except:
        return df[df.index == '0']


