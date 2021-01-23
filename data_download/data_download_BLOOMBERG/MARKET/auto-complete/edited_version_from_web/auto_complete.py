import requests
import pandas as pd
import numpy as np
import datetime


def extract_ticks(interval="m1"):
    url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-chart"

    querystring = {"interval":interval,"id":"ibm%3Aus"}

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

with open ("data_log_auto_complete_json.json", "w") as plik:
	print(json_d, file=plik)

df = pd.json_normalize(json_d['result'])
df_t = df.T

df_t.to_excel("structured_data_auto_complete.xlsx")

