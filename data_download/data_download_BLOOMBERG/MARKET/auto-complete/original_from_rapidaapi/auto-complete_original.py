import requests
import pandas as pd
import numpy as np
import datetime
import json

url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/auto-complete"

querystring = {"query":"ibm"}

headers = {
    'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e",
    'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

row_data = response.text

with open ("data_log_original_version.txt", "w") as plik:
	print(row_data, file=plik)

d = json.loads(row_data)

with open ("data_log_original_version_json.json", "w") as plik:
	print(d, file=plik)

df = pd.json_normalize(d['quote'])
df_t = df.T

df_t.to_excel("structured_data_original_version.xlsx")