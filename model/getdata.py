import pandas as pd
import yfinance as yf
import datetime  as datetime
import model.mydb as mydb

histEndDate = '2022-10-01'

def getData(stock, startDate, endDate):
    if endDate < datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getHistData(stock, startDate, endDate)

    if startDate >= datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getYahooData(stock, startDate)

    return pd.concat([getHistData(stock, startDate, datetime.datetime.strptime(histEndDate, '%Y-%m-%d')), 
            getYahooData(stock, datetime.datetime.strptime(histEndDate, '%Y-%m-%d'))])

def getHistData(stock, startDate, endDate):
    saveFile = r'data/k' + stock + '.tw.csv'
    
    data = pd.read_csv(saveFile,  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    return data[data.index>startDate][data[data.index>startDate].index<endDate]

def getYahooData(stock, startDate):
    df = yf.download(stock +".tw", start = startDate)
    #updateHistData
    if len(df)>0 and not mydb.is_update_stockhist(stock):
        #print('update' + stock)
        pd.concat([getHistData(stock, '2012-01-01', startDate), df]
                    ).to_csv(r'data/k' + stock.lower() + '.tw.csv')
        mydb.has_update_stockhist(stock)
    #else:
        #print('not update' + stock) 
    return df
    
def getStockInfo(stock):
    df = pd.read_csv(r'data/stocklist.csv', header=0, index_col='stockId')
    df.index = df.index.map(str)

    try:
        data = df[df.index == stock]
        if df[df.index == stock].empty:
            return df[df.index == '0']
        else:
            return df[df.index == stock]
    except:
        return df[df.index == '0']


