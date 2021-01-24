import yfinance as yf
import json
import pandas as pd
import openpyxl
import datetime as dt
import os

df = pd.read_excel('Revolut_ticker_test.xlsx')
tickers=df['tickers'].tolist()

start="2019-07-01"
end=dt.datetime.now()

errors=[]

def data_scraping():
    df = pd.read_excel('attributes.xlsx')
    attributes=df['attributes'].tolist()
    for attribute in attributes:
        try:
            x = getattr(yeah, attribute)
            x.to_csv("stock_data/{}/{}.csv".format(ticker, attribute), sep='\t')
            x.to_excel("stock_data/{}/{}.xlsx".format(ticker, attribute))
        except KeyError as e:
            errors.append("{} for {}: {}".format(attribute, ticker, e))
            print("{} for {}: {}".format(attribute, ticker, e))
        except KeyError as i:
            errors.append("{} for {}: {}".format(attribute, ticker, i))
            print("{} for {}: {}".format(attribute, ticker, i))
        except Exception as inst:
            print("{} for {}: {}".format(attribute, ticker, inst))
            errors.append("Niezidentyfikowany error dla {}: {}".format(ticker, inst))


for ticker in tickers:
    if not os.path.exists('stock_data/{}'.format(ticker)):
        os.makedirs('stock_data/{}'.format(ticker))
        
        try:
            data=yf.download(ticker,start,end,interval='1h',prepost=True, group_by = 'ticker')
            data.to_csv(('stock_data/{}/{}.csv'.format(ticker, ticker)), sep='\t')
            data.to_excel(('stock_data/{}/{}.xlsx'.format(ticker, ticker)))
        except KeyError as e:
            errors.append("Main data for {}: {}".format(ticker, e))
            print("Main data for {}: {}".format(ticker, e))
        except KeyError as i:
            errors.append("Main data for {}: {}".format(ticker, i))
            print("Main data for {}: {}".format(ticker, i))
        except Exception as inst:
            print("Main data for {}: {}".format(ticker, inst))
            errors.append("Niezidentyfikowany error dla {}: {}".format(ticker, inst))
        
        yeah = yf.Ticker("{}".format(ticker))
        
        
        try:
            inf = yeah.info    
            with open ("stock_data/{}/{}_info.txt".format(ticker, ticker), "w") as f:
                for k, v in inf.items():
                    print((str(k) + ' >>> '+ str(v)), file=f)
        except KeyError as e:
            errors.append("Info data for {}: {}".format(ticker, e))
            print("Info data for {}: {}".format(ticker, e))
        except KeyError as i:
            errors.append("Info data for {}: {}".format(ticker, i))
            print("Info data for {}: {}".format(ticker, i))
        except Exception as inst:
            print("Info data for {}: {}".format(ticker, inst))
            errors.append("Niezidentyfikowany error dla {}: {}".format(ticker, inst))
            
            
        try:
            hist = yeah.history(period="max")
            hist.to_csv("stock_data/{}/history.csv".format(ticker), sep='\t')
            hist.to_excel("stock_data/{}/history.xlsx".format(ticker))
        except KeyError as e:
            errors.append("History data for {}: {}".format(ticker, e))
            print("History data for {}: {}".format(ticker, e))
        except KeyError as i:
            errors.append("History data for {}: {}".format(ticker, i))
            print("History data for {}: {}".format(ticker, i))
        except Exception as inst:
            print("History data for {}: {}".format(ticker, inst))
            errors.append("Niezidentyfikowany error dla {}: {}".format(ticker, inst))
            
            
        data_scraping()
        
        
        try:
            isin = yeah.isin
            with open ('stock_data/{}/isin.txt'.format(ticker),'w') as plik:
                print(isin, file=plik)
        except KeyError as e:
            errors.append("Isin data for {}: {}".format(ticker, e))
            print("Isin data for {}: {}".format(ticker, e))
        except KeyError as i:
            errors.append("Isin data for {}: {}".format(ticker, i))
            print("Isin data for {}: {}".format(ticker, i))
        except Exception as inst:
            print("Isin data for {}: {}".format(ticker, inst))
            errors.append("Niezidentyfikowany error dla {}: {}".format(ticker, inst))
        
        try:
            options = str(yeah.options)
            with open ('stock_data/{}/options.txt'.format(ticker),'w') as f2:
                print(options, file=f2)
        except KeyError as e:
            errors.append("Options data for {}: {}".format(ticker, e))
            print("Options data for {}: {}".format(ticker, e))
        except KeyError as i:
            errors.append("Options data for {}: {}".format(ticker, i))
            print("Options data for {}: {}".format(ticker, i))
        except Exception as inst:
            print("Options data for {}: {}".format(ticker, inst))
            errors.append("Niezidentyfikowany error dla {}: {}".format(ticker, inst))
                  
    else:
        print('Already have {}'.format(ticker))

print(errors)

with open ("errors.txt", "w") as plik:
            for err in errors:
                print(str(err), file=plik)