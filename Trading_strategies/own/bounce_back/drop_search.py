#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime,date
import functions as fun
import openpyxl

#turns off chained assignment warnings
pd.options.mode.chained_assignment = None

check = -10 #drop threshold to be searched
period = 7  #number of hours within the drop is being searched

df = pd.read_excel('stock_data/AAL/AAL.xlsx')

#check datatype of the column
#print(df['Close'].dtype)

fun.hours_column_add(df)
df = df[['Date', 'Hours', 'Open', 'High','Low', 'Close', 'Adj Close', 'Volume']]

def drop_edge_dates(time_window_df, length):
    beginning_date = time_window_df.iat[0,0]
    #print(beginning_date)
    beginning_hour = time_window_df.iat[0,1]
    #print(beginning_hour)
    
    end_date = time_window_df.iat[length-1,0]
    #print(end_date)
    end_hour = time_window_df.iat[length-1,1]
    #print(end_hour)
    
    wbk=load_workbook(filename = 'output_template.xlsx')
    wks=wbk.active
    wks['B14']= beginning_date
    wks['C14']= end_date
    wbk.save("output_template.xlsx")



#the row to be checked
x=0

for y in range(len(df.index)):
    #test window definition
    test_window = df[x : x+period]
    
    if y == 0:
        print(test_window.head(15))
    
    #firs value of Open column
    start_point = test_window.iat[0,2]
    #last value of Close column
    end_point = test_window.iat[-1,5]
    
    result = fun.percentage(end_point, start_point)
    
    if result < check:
        print(result)
        
        fun.plot(df, x, check)
        
        
        drop_edge_dates(test_window, period)
        
        #skip 30 rows after drop finding (not to repead for the same event)
        x+=30
    
    else:
        x+=1

    