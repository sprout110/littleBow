from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
yf.pdr_override()
import pandas as pd

# Tickers list
# We can add and delete any ticker from the list to get desired ticker live data
ticker_list=['DJIA', 'DOW', 'LB', 'EXPE', 'PXD', 'MCHP', 'CRM' , 'NRG', 'NOW']

today = date.today()

# We can get data by our choice by giving days bracket
start_date= "2017–01–01"
end_date="2022–11–30"

files=[]
def getData(ticker):
	print(ticker)
	data = pdr.get_data_yahoo(ticker, start=start_date, end=today)
	dataname= ticker+'_'+str(today)
	files.append(dataname)
	SaveData(data, dataname)

# Create a data folder in your current dir.
def SaveData(df, filename):
	df.to_csv('./data/'+filename+'.csv')

#This loop will iterate over ticker list, will pass one ticker to get data, and save that data as file.

for tik in ticker_list:
	getData(tik)

for i in range(0,11):
	df1= pd.read_csv('./data/'+ str(files[i])+'.csv')
print (df1.head())

# Let us take the results for Facebook and hence using “FB”.

# Here We are getting Facebook financial information
# We need to pass FB as argument for that
GetFacebookInformation = yf.Ticker("FB")
 
# whole python dictionary is printed here
print(GetFacebookInformation.info)


# 2412.TW
GetCHTInformation = yf.Ticker("2412.TW")
print(GetCHTInformation.info)

# display Company Sector
print("Company Sector : ", GetCHTInformation.info['sector'])
 
# display Price Earnings Ratio
print("Price Earnings Ratio : ", GetCHTInformation.info['trailingPE'])
 
# display Company Beta
print(" Company Beta : ", GetCHTInformation.info['beta'])

# get all key value pairs that are available
for key, value in GetCHTInformation.info.items():
    print(key, ":", value)

# Let us  get historical stock prices for CHT
# covering the past few years.
# max->maximum number of daily prices available
# for CHT.
# Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y,
# 5y, 10y and ytd.
print(GetCHTInformation.history(period="max"))

# Let us check out for 6 months
print(GetCHTInformation.history(period="6mo"))

#----------------------------------------------------------------
# in order to specify start date and
# end date we need datetime package
import datetime
 
# startDate , as per our convenience we can modify
startDate = datetime.datetime(2021, 1, 1)
 
# endDate , as per our convenience we can modify
endDate = datetime.datetime(2022, 11, 30)
 
# pass the parameters as the taken dates for start and end
print(GetCHTInformation.history(start=startDate, end=endDate))


# -------------------------------------------------
# Plot historical prices
# pip install matplotlib
# pip install seaborn

import matplotlib.pyplot as plt
import seaborn

# get historical market data
hist = GetCHTInformation.history(period="5d")

# Plot everything by leveraging the very powerful matplotlib package
hist['Close'].plot(figsize=(16, 9))

plt.show()

# Download stock data then export as CSV
data_df = yf.download("2412.TW", start="2020-02-01", end="2020-03-20")
data_df.to_csv('2412.csv')

# 2412.TW
CHT = yf.Ticker("2412.TW")
# Change period to last full year
CHT.history(period="1y")
# show actions (dividends, splits)
CHT.actions