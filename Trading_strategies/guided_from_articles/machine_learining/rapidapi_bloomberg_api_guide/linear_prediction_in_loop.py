#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Summary of python script.

#===============================================================
#% DESCRIPTION
#%    Script fetched the data form previously prepared json file.
#%    Then the data is modified and passed to sklearn algorithm, which creates model
#%    of predicion.
#%
#% Usage: linear_prediction_in_loop.py ticker --implemented
#%
#%    ticker - ticker of a company - tsla, all, aapl, nkla
#%
#===============================================================
#- IMPLEMENTATION
#-    version         1.0.0
#-    author          Michał Konik
#-    copyright       GNU General Public License
#-
#===============================================================
#  HISTORY
#     24/01/2021 : first implementation
#
#===============================================================
#  CREDITS
#    Inspired by Michel VONGVILAY's bash script template -
#        - GNU General Public License
#    +
#    Rapidapi.com website.
#
#===============================================================
"""

import pandas as pd
import datetime
import json
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import fnmatch

#read tickers form a xlsx file
try:
    df = pd.read_excel('revolut_ticker_test.xlsx')
    #print(df)
    rev_tickers=df['tickers'].tolist()
except (OSError, IOError, KeyError, Exception) as err:
        print("Error message: {}".format(err))
        exit(1)

errors = []
loop = len(rev_tickers) + 1
for ticker in rev_tickers:
    loop = loop - 1

    input_file_name = "{}_y5.json".format(ticker)

    #load the saved JSON response in Pandas DataFrame.
    try:
        with open("stock_data/{}/{}".format(ticker, input_file_name),"r") as fp:
            json_d = json.load(fp)
    except (OSError, IOError, KeyError, Exception) as err:
            print("Error message for the {} ticker: {}".format(ticker, err))
            exit(1)


    try:
        ticks_d = json_d['result']['{}:US'.format(ticker)]['ticks']   #ticker to be changed here for the current one
        df = pd.DataFrame(ticks_d)
        df['Close'] = df['close']
        df['Date'] = df['time'].apply(lambda x:datetime.datetime.fromtimestamp(x))
        df = df.set_index('time')
        data = df.sort_index(ascending=True, axis=0)
        #print(data)

        #Cleanse the Data to Retain Only the Most Important Information
        #creating a separate dataset
        new_data = data[['Date','Close']]
        index = range(0,len(new_data))
        new_data['index']=index
        new_data=new_data.set_index('index')
        new_data['Date'] = pd.to_datetime(new_data.Date,format='%Y-%m-%d')
        #print(new_data)

        #Add Additional Features to the Data Set:
        #precisely the data set that identify a given date as beginning or end of a week, month, quarter, or year. 
        # In addition to that, we also add extra columns to contain the day, month, and year.
        def adddatepart(data,col):
            data['month'] = data[col].dt.month
            data['day'] = data[col].dt.day
            data['year'] = data[col].dt.year
            data['quarter'] = data[col].dt.quarter
            data['dayofweek'] = data[col].dt.dayofweek
            data['dayofyear'] = data[col].dt.dayofyear
            #data['dayinmonth'] = data[col].dt.daysinmonth
            data['is_month_end'] = data[col].dt.is_month_end.astype(int)
            data['is_month_start'] = data[col].dt.is_month_start.astype(int)
            data['is_quarter_start'] = data[col].dt.is_quarter_start.astype(int)
            data['is_quarter_end'] = data[col].dt.is_quarter_end.astype(int)
            data['is_year_start'] = data[col].dt.is_year_start.astype(int)
            data['is_year_end'] = data[col].dt.is_year_end.astype(int)
            data['mon_fri'] = data['dayofweek'].apply(lambda x: 1 if x==0 or x==4 else 0)
            return data
            
        adddatepart(new_data,'Date')
        #print(new_data)
        new_data.to_excel("stock_data/{}/{}_5y_df_log_maching_learining_input.xlsx".format(ticker, ticker))

        #Split the Data Set into X and Y
        X = new_data.drop('Date',axis=1)
        X.drop('Close',axis=1,inplace=True)
        #print(X)

        Y = new_data['Close']
        #print(Y)

        #Split the Data into Training and Testing Set
        #we teach the nauron network only 70% of the data, and use the remaining 30% to eveluate the result that we get
        train_pct_index = int(0.7 * len(X))
        x_train, x_validate = X[:train_pct_index], X[train_pct_index:]
        y_train, y_validate = Y[:train_pct_index], Y[train_pct_index:]

        #Train a Linear Regression-Based Model with the Training Set
        model = LinearRegression()
        model.fit(x_train,y_train)

        #Test the Prediction Model
        #make predictions and find the rmse
        preds = model.predict(x_validate)
        rms=np.sqrt(np.mean(np.power((np.array(y_validate)-np.array(preds)),2)))
        # This gives the accuracy of the model, the lesser the better
        #print("Rms linear reg",rms)


        #Plot the Model’s Prediction Performance
        viz_data = new_data[['Date','Close']]
        viz_data['Predictions'] = 0
        for i in range(train_pct_index,len(viz_data)):
            viz_data.loc[i,'Predictions'] = preds[i-train_pct_index]
        #print(viz_data)
        viz_data.to_excel("stock_data/{}/{}_5y_df_log_with_predictions.xlsx".format(ticker, ticker))

        fig= plt.figure(figsize=(20,10))
        dates = viz_data['Date'][train_pct_index:]
        plt.plot(dates, viz_data['Close'][train_pct_index:], c='k', label='Actual Data')
        plt.plot(dates, preds, c='g', label='Linear model')

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Linear Regression of Stock Prediction')
        plt.grid()
        plt.legend()
        plt.savefig("stock_data/{}/{}_5y_prediction_chart.png".format(ticker, ticker))
        #plt.show()
        
        print("Awesome data logged. Left only: {} tickers!". format(loop))

    except KeyError as e:
        errors.append("{} encountered: {}".format(ticker, e))
        print("{} encountered: {}".format(ticker, e))
    except KeyError as i:
        errors.append("{} encountered: {}".format(ticker, i))
        print("{} encountered: {}".format(ticker, i))
    except Exception as inst:
        errors.append("{} encountered: {}".format(ticker, inst))
        print("{} encountered: {}".format(ticker, inst))