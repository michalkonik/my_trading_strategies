#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Summary of python script.

#===============================================================
#% DESCRIPTION
#%    Script download data from Bloomberg API, for passed ticker with for passed time period.
#%
#% Usage: extract_data_main.py ticker time_period
#%
#%    ticker - ticker of a company - tsla, all, aapl, nkla
#%    time_period - time period for which we want to download a data - d1|d3|ytd|m1|m3|m6|y1|y5
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
import argparse

#parse arguments passed while running the script from cmd
parser = argparse.ArgumentParser()
parser.add_argument("ticker", help="ticker of a company - tsla, all, aapl, nkla")
parser.add_argument("time_period", help="time period for which we want to download a data - d1|d3|ytd|m1|m3|m6|y1|y5")
args = parser.parse_args()


def extract_ticks(interval="y5"):
    url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-chart"

    querystring = {"interval":interval,"id": "{}%3Aus".format(args.ticker)}

    headers = {
        'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com",
        'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_d = response.json()
    return json_d

#Get year to date data ytd
json_d = extract_ticks(args.time_period)
print(json_d)

# Write the data to json file
with open("{}_{}.json".format(args.ticker, args.time_period),"w") as fp:
    json.dump(json_d,fp)
