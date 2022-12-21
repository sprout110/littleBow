import pandas as pd
import yfinance as yf

def getStockData(startDate='2022-01-01', endDate='2022-12-17'):
    data = pd.read_csv(r'data/k2412-2005-2022.csv',  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    return data[data.index>startDate][data[data.index>startDate].index<endDate]

def getYahooData(stock, startTime):
    return yf.download(stock, start = startTime)


