import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime,date

#turns off chained assignment warnings
pd.options.mode.chained_assignment = None

check = -15 #drop threshold to be searched
period = 8  #number of hours within the drop is being searched

df = pd.read_excel('AAL\AAL.xlsx')

#check datatype of the column
#print(df['Close'].dtype)

#percentage drop/increase computing
#arguments in order: last and first values of meassured period
def percentage(part, whole):
    perc = 100 * float(part)/float(whole)
    perc = perc - 100
    return perc
  
#plot of a chart of the market reaction to the price drop
#arguments in order: df, numer of line where the drop began, threshold to be checked
def plot(data_frame, whereami, drop_threshold):
    #numer of dates before and after drop to be ploted
    market_reaction = data_frame[whereami-30: whereami+150]
    
    #datatime to str type conversion
    market_reaction['Date'] = market_reaction['Date'].astype(str)
    
    #size of the plot and axis assignment
    fig, ax = plt.subplots(figsize=(15, 9))

    #chart definition - can be multiple to reflect different arrays
    ax.plot(market_reaction.index, market_reaction['Open'], marker='s', linestyle='--', color='green')
    #ax.plot(market_reaction.index, market_reaction['Close'], marker='v', linestyle='--', color='blue')

    ax.set_xlabel("Timeline")
    ax.set_ylabel("Share's Price")
    ax.set_title("Market reaction after 15% drop")
    
    #vertical line definition - end of meassured drop
    plt.axvline(x=whereami+7, ymin=0.0, ymax=1.0, color='red', linestyle='--', alpha=0.3)
    trans = ax.get_xaxis_transform()
    plt.text(whereami+5, 1.01, str(drop_threshold), transform=trans, color='red')
    
    #vertical line definition - start of meassured drop
    plt.axvline(x=whereami, ymin=0.0, ymax=1.0, color='blue', linestyle='--', alpha=0.3)
    trans_2 = ax.get_xaxis_transform()
    plt.text(whereami-1, 1.01, "Beginning", transform=trans_2, rotation='vertical', color='blue')

    #description of x axis definition (dates)
    plt.xticks(market_reaction.index, market_reaction['Date'].astype(str), rotation=20)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(7))

    plt.savefig('{}_drop_{}_pp_market_reaction.pdf'.format(market_reaction.iloc[0]['Date'], abs(drop_threshold)))
   
#the row to be checked
x=0

for y in range(len(df.index)):
    #test window definition
    test_window = df[x : x+period-1]
    try:
        #firs value of Open column
        start_point = test_window.iat[0,1]
        #last value of Close column
        end_point = test_window.iat[-1,4]
        
        result = percentage(end_point, start_point)
        
        if result < check:
            print(result)
            
            plot(df, x, check)
            
            #skip 30 rows after drop finding (not to repead for the same event)
            x+=30
        
        else:
            x+=1

    except:
        pass