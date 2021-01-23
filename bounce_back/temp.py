#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime,date
import functions as fun

#turns off chained assignment warnings
pd.options.mode.chained_assignment = None

check = -15 #drop threshold to be searched
period = 7  #number of hours within the drop is being searched

df = pd.read_excel('AAL\AAL.xlsx')

#check datatype of the column
#print(df['Close'].dtype)

fun.hours_column_add(df)
df = df[['Date', 'Hours', 'Open', 'High','Low', 'Close', 'Adj Close', 'Volume']]

def drop_edge_dates(time_window_df, length):
    beginning_date = time_window_df.iat[0,0]
    beginning_hour = time_window_df.iat[0,1]
    
    end_date = time_window_df.iat[length-1,0]
    end_hour = time_window_df.iat[length-1,1]
    



#the row to be checked
x=0

for y in range(len(df.index)):
    #test window definition
    test_window = df[x : x+period]
    try:
        #firs value of Open column
        start_point = test_window.iat[0,2]
        #last value of Close column
        end_point = test_window.iat[-1,5]
        
        result = fun.percentage(end_point, start_point)
        
        if result < check:
            print(result)
            
            fun.plot(df, x, check)
            
            
            #drop_edge_dates(test_window, period)
            
            #skip 30 rows after drop finding (not to repead for the same event)
            x+=30
        
        else:
            x+=1

    except:
        pass