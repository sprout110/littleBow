import requests
import pandas as pd
import yfinance as yf
import datetime

def get_stock_hist(stock, startDate, endDate):
    stock = stock +".tw"
    return yf.download(stock, start = startDate, end=endDate)

stock = '1216'
taiwan_stock = get_stock_hist(stock, '2012-01-01', '2022-10-01')
taiwan_stock.to_csv('data/k' + str(stock) + '.csv')