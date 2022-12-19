import requests
import pandas as pd

def get_stock_list():
  res = requests.get("https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y")
  df = pd.read_html(res.text)[0]        # Parse the Source Code into a Pandas DataFrame
  df = df.drop([0,1,4,5,8,9],axis = 1)  # Drop Useless Columns
  df.columns = df.iloc[0]               # Replace DataFrame Columns Title
  df = df.iloc[1:]
  return df

def create_date_list(start_date, stop_date="2020/10/10"):
  start_time = start_date.split("/")
  stop_time = stop_date.split("/")
  date_list = []
  for i in range(int(start_time[1]), 13):
    date_list.append(str(int(start_time[0])*10000+i*100+1))
  for i in range(int(start_time[0])+1,int(stop_time[0])):
    for j in range(1,13):
      date_list.append(str(i*10000+j*100+1))
  for i in range(1, int(stop_time[1])+1):
    date_list.append(str(int(stop_time[0])*10000+i*100+1))
  return date_list

def get_monthly_stock_history(date, stock_no):
  quotes = []
  url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, stock_no)
  r = requests.get(url)
  data = r.json()
  if data['stat'] == 'OK':
    df = pd.DataFrame(data['data'], columns = data['fields'])
    return df
  else:
    print("Request Failed!! Stat:", data['stat'])

taiwan_stock = get_stock_list()

#taiwan_stock.to_csv('test.csv')

import yfinance as yf


def plot_stcok_k_chart(stock='2412.tw', startTime ='2005-01-01'):

    df = yf.download(stock, start = startTime)
    return df
stock = '2412'
startTime = '2010-01-01'
#df = yf.download(stock, start = startTime)
df = plot_stcok_k_chart()
#result = get_monthly_stock_history('2005', '2412')
#result.to_csv('2014.cvs')

df.to_csv('2412.csv')


'''
for i in range(crawl_head, crawl_tail):
  result = pd.DataFrame()
  release_date = taiwan_stock.iloc[i]["公開發行/上市(櫃)/發行日"]
  if int(release_date.split("/")[0]) < 2010:
    query_date = "2010/10/10"
  else:
    query_date = release_date
  date_list = create_date_list(query_date)
  
  for d in date_list:
    clear_output(wait=True)
    print("Processing:", i, "Stock No.", taiwan_stock.iloc[i]["有價證券代號"], "Date:", d)
    result = pd.concat([result, get_monthly_stock_history(d, taiwan_stock.iloc[i]["有價證券代號"])], axis=0)
    time.sleep(random.randint(5,10))

  result.to_csv("/mydrive/" + taiwan_stock.iloc[i]["有價證券代號"] + ".csv")
'''

