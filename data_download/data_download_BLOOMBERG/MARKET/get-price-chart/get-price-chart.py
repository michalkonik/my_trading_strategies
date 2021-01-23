import requests
import json
import pandas as pd

url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-price-chart"

querystring = {"id":"inmex:ind","interval":"d1"}

headers = {
    'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e",
    'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

row_data = response.text
print(type(row_data))

with open ("data_log_price_chart.txt", "w") as plik:
	print(row_data, file=plik)

d = json.loads(row_data)

with open ("data_log_price_chart_json.json", "w") as plik:
	print(d, file=plik)

df = pd.json_normalize(d['result'])
df_t = df.T

df_t.to_excel("structured_data_price_chart.xlsx")