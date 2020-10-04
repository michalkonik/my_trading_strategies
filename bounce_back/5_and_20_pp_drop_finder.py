import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime,date

pd.options.mode.chained_assignment = None

df = pd.read_excel('AAL\AAL.xlsx')

#convert datatype of the column to str
#df['Date'] = df['Date'].astype(str)

#check datatype of the column
#print(df.Close.dtype)

def percentage(part, whole):
    perc = 100 * float(part)/float(whole)
    perc = perc - 100
    return perc
  
   
x=0
for y in range(len(df.index)):
    #len(df.index)  - ilość wierszy, czyli potrzebnych iteracji   
    osiem_h_open = df[x : x+7]
    try:
        #pierwsza pozycja z kolumny open
        start_point = osiem_h_open.iat[0,1]
        #ostatnia pozycja z kolumny close
        end_point = osiem_h_open.iat[-1,4]

        #print(start_point)
        #print(end_point)
        #print('\n')
        
        result = percentage(end_point, start_point)
        
        if result < -15:
            print(result)
            
            
            market_reaction = df[x-30: x+150]
            x+=30 
            #print(market_reaction)
            #print(market_reaction['Date'])
            
            market_reaction['Date'] = market_reaction['Date'].astype(str)
            
            fig, ax = plt.subplots(figsize=(15, 9))

            ax.plot(market_reaction.index, market_reaction['Open'], marker='s', linestyle='--', color='green')
            #ax.plot(market_reaction.index, market_reaction['Close'], marker='v', linestyle='--', color='blue')

            ax.set_xlabel("when exactly")
            ax.set_ylabel("price")
            ax.set_title("what happens after 15% drop")
            
            plt.axvline(x=x-23, ymin=0.0, ymax=1.0, color='red', linestyle='--', alpha=0.3)
            plt.axvline(x=x-30, ymin=0.0, ymax=1.0, color='blue', linestyle='--', alpha=0.3)

            plt.xticks(market_reaction.index, market_reaction['Date'].astype(str), rotation=20)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(7))

            plt.savefig('plot_{}.pdf'.format(market_reaction.iloc[0]['Date']))
        
        else:
            x+=1

    except:
        pass