
import yfinance as yf

#define the ticker symbol
tickerSymbol = 'AAPL'
#tickerSymbol = 'GOOGL'

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#stock_info = tickerData.info
#print(stock_info.keys())
print(tickerData.info['currency'])

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1mo', start='1980-12-12', end='1980-12-20')
#tickerDf = tickerData.history(period='1mo', start='2004-08-19', end='2004-09-19')

#see your data
#print(type(tickerDf))

#print(tickerDf.info)

# first 5
print(tickerDf)
df = tickerDf.head(5)
#print(type(df))
print(df)
print(len(df.index))

#item = df.iloc[0]

#Open_1 = item.Open
#print(Open_1)

#Close_2 = item.Close
#print(Close_2)