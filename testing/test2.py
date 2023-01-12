# from model.selectbot import UserSay

# Bot = UserSay("uid", "k2412")
# print(Bot.dosomething())

from  FinMind.data import DataLoader
import datetime

FM = DataLoader()
stock = '4205'
endDate = datetime.datetime.today().strftime('%Y-%m-%d')
print(endDate)
df=FM.taiwan_stock_daily_adj(stock_id=stock, start_date=endDate, end_date=endDate)
#Date,Open,High,Low,Close,Adj Close,Volume
df=df.rename(columns={'date':'Date', 'open':'Open', 'max':'High', 'min':'Low', 'close':'Close', 'Trading_Volume':'Volume'})
df = df[['Date','Open','High','Low','Close','Volume']]
df.set_index('Date', inplace=True)
print(df.head(5))

#df.to_csv('k' + stock + '.tw.csv')

