import pandas as pd
import yfinance as yf
import datetime  as datetime
import model.mydb as mydb

histEndDate = '2023-01-01'

def getData(stock, startDate, endDate):
    if endDate < datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getHistData(stock, startDate, endDate)

    if startDate >= datetime.datetime.strptime(histEndDate, '%Y-%m-%d'):
        return getYahooData(stock, startDate)

    # temp1 = getHistData(stock, startDate, datetime.datetime.strptime(histEndDate, '%Y-%m-%d'))
    # print(temp1.tail(5))
    # temp2 = getYahooData(stock, datetime.datetime.strptime(histEndDate, '%Y-%m-%d'))
    # print(temp2.tail(5))

    return pd.concat([getHistData(stock, startDate, datetime.datetime.strptime(histEndDate, '%Y-%m-%d')), 
            getYahooData(stock, datetime.datetime.strptime(histEndDate, '%Y-%m-%d'))])

def getHistData(stock, startDate, endDate):
    saveFile = r'k' + stock + '.tw.csv'
    # print(saveFile)
    data = pd.read_csv(saveFile,  header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    # print(data.head(5))
    # print(data[data.index>startDate][data[data.index>startDate].index<endDate])
    return data[data.index>startDate][data[data.index>startDate].index<endDate]

def getYahooData(stock, startDate):
    df = yf.download(stock +".tw", start = startDate)
    # print(startDate)
    # print(df.head(5))
    #updateHistData
    if df.shape[0]>0 and not mydb.is_update_stockhist(stock):
        saveFile = r'k' + stock + '.tw.csv'
        pd.concat([getHistData(stock, '2002-01-01', startDate), df]
                    ).to_csv(saveFile)
        mydb.has_update_stockhist(stock)
    #else:
        #df = pd.DataFrame()
    return df
    
def getStockInfo(stock):
    df = pd.read_csv(r'stocklist.csv', converters={'stockId': str})
    df.set_index("stockId" , inplace=True)
   
    if df[df.index == stock].empty:
        return df[df.index == '0000']
    else:
        return df[df.index == stock]



