import requests
import pandas as pd
import numpy as np
import datetime
import json


def extract_ticks(interval="y1"):
    url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-chart"

    querystring = {"interval":interval,"id":"aal%3Aus"}

    headers = {
        'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com",
        'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_d = response.json()
    return json_d

#Get year to date data ytd
json_d = extract_ticks()
print(json_d)

# Write the data to json file
with open("ibm_ytd.json","w") as fp:
    json.dump(json_d,fp)
