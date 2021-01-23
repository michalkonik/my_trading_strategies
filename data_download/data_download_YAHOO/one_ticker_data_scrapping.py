import yfinance as yf
import datetime as dt

start="2016-01-01"
end=dt.datetime.now()

ticker= "AAPL"

data=yf.download(ticker,start,end,interval='1h')
data.to_csv(('{}.csv'.format(ticker, ticker)), sep='\t')
data.to_excel(('{}.xlsx'.format(ticker, ticker)))