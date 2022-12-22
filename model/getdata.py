import pandas as pd
import yfinance as yf

def getStockData(startDate='2022-01-01', endDate='2022-12-17'):
    data = pd.read_csv(r'data/k2412-2005-2022.csv',  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    return data[data.index>startDate][data[data.index>startDate].index<endDate]

def getYahooData(stock, startTime):
    stock = stock +".tw"
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


