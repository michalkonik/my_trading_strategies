import requests
import json
import pandas as pd

url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/market/get-cross-currencies"

querystring = {"id":"aed,aud,brl,cad,chf,cnh,cny,cop,czk,dkk,eur,gbp,hkd,huf,idr,ils,inr,jpy,krw,mxn,myr,nok,nzd,php,pln,rub,sek,sgd,thb,try,twd,usd,zar"}

headers = {
    'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e",
    'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

row_data = response.text
print(type(row_data))

with open ("data_log_currencies.txt", "w") as plik:
	print(row_data, file=plik)

d = json.loads(row_data)

with open ("data_log_currencies_json.json", "w") as plik:
	print(d, file=plik)

df = pd.json_normalize(d['result'])
df_t = df.T

df_t.to_excel("structured_data_currencies.xlsx")