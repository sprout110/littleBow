import pandas as pd
import yfinance as yf
from  FinMind.data import DataLoader
FM = DataLoader()
import datetime  as datetime
import model.mydb as mydb

histEndDate = '2023-01-01'

def getData(stock, startDate, endDate):
    if endDate <= datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getHistData(stock, startDate, endDate)

    if startDate >= datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        df = getYahooData(stock, startDate)
        #print(df)
        #df.set_index("Date" , inplace=True)
        #df.index = pd.to_datetime(df.index)
        #print(df[df.index<endDate])
        return df[df.index<endDate]

    #temp1 = getHistData(stock, startDate, datetime.datetime.strptime(histEndDate, '%Y-%m-%d'))
    #print(temp1.tail(5))
    temp2 = getYahooData(stock, datetime.datetime.strptime(histEndDate, '%Y-%m-%d'))
    #print(temp2.tail(5))

    return pd.concat([getHistData(stock, startDate, datetime.datetime.strptime(histEndDate, '%Y-%m-%d')), 
            temp2[temp2.index<endDate]])

def getHistData(stock, startDate, endDate):
    saveFile = r'k' + stock + '.tw.csv'
    #print(saveFile)
    data = pd.read_csv(saveFile,  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    #print(data.head(5))
    # print(data[data.index>startDate][data[data.index>startDate].index<endDate])
    # print(data[data.index>=startDate])
    #print(data[data.index>=startDate][data[data.index>=startDate].index<endDate])
    return data[data.index>=startDate][data[data.index>=startDate].index<endDate]

def getYahooData(stock, startDate):
    return yf.download(stock +".tw", start = startDate)
    
def getStockInfo(stock):
    df = pd.read_csv(r'stocklist.csv', converters={'stockId': str})
    df.set_index("stockId" , inplace=True)
   
    if df[df.index == stock].empty:
        return df[df.index == '0000']
    else:
        return df[df.index == stock]



