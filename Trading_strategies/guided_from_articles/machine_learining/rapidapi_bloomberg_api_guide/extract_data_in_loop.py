#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Summary of python script.

#===============================================================
#% DESCRIPTION
#%    Script download data from Bloomberg API, for tickers fetched from xlsx file for last 5 yesrs.
#%
#% Usage: python extract_data_main.py
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

import requests
import pandas as pd
import numpy as np
import json
import os

def extract_ticks(company, interval="y5"):
    url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-chart"

    querystring = {"interval":interval,"id": "{}%3Aus".format(company)}

    headers = {
        'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com",
        'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_d = response.json()
    return json_d


errors=[]

try:
    df = pd.read_excel('revolut_ticker_test.xlsx')
    #print(df)
    rev_tickers=df['tickers'].tolist()
except (OSError, IOError, KeyError, Exception) as err:
        print("Error message: {}".format(err))
        exit(1)

loop = len(rev_tickers) + 1
for ticker in rev_tickers:
    if not os.path.exists('stock_data/{}'.format(ticker)):
        os.makedirs('stock_data/{}'.format(ticker))
        try:
            loop = loop - 1
            json_d = extract_ticks(ticker)
            #print(json_d)

            # Write the data to json file
            with open("stock_data/{}/{}_y5.json".format(ticker, ticker),"w") as fp:
                json.dump(json_d,fp)

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


with open ("errors.txt", "w") as plik:
            for err in errors:
                print(str(err), file=plik)