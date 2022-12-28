import pandas as pd
import yfinance as yf
import datetime  as datetime

histEndDate = '2022-10-01'

def getData(stock, startDate, endDate):
    if startDate >= datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getYahooData(stock, startDate, endDate)
    if endDate < datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getStockData(stock, startDate, endDate)

    df1 = getStockData(stock, startDate, endDate)
    df2 = getYahooData(stock, startDate, endDate)
    #print(df1.tail(3))
    #print(df2.head(3))
    return pd.concat([df1, df2])

def getStockData(stock, startDate='2022-01-01', endDate='2022-10-01'):
    if endDate >= datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        endDate = datetime.datetime.strptime(histEndDate, '%Y-%m-%d')
    saveFile = r'data/k' + stock + '.csv'
    data = pd.read_csv(saveFile,  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    return data[data.index>startDate][data[data.index>startDate].index<endDate]

def getYahooData(stock, startTime, endTime):
    stock = stock +".tw"
    if startTime < datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        startTime = datetime.datetime.strptime(histEndDate, '%Y-%m-%d')
    return yf.download(stock, start = startTime, end = endTime)

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


