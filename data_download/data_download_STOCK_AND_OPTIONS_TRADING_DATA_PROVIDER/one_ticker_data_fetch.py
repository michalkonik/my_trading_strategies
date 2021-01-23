import http.client
import pandas as pd

conn = http.client.HTTPSConnection("stock-and-options-trading-data-provider.p.rapidapi.com")

headers = {
    'x-rapidapi-proxy-secret': "a755b180-f5a9-11e9-9f69-7bf51e845926",
    'x-rapidapi-key': "a9164563cbmshbb0d9669c26e1e6p1c432bjsn477e1068516e",
    'x-rapidapi-host': "stock-and-options-trading-data-provider.p.rapidapi.com"
    }

#tutaj podmianiamy tickery 
conn.request("GET", "/options/tsla", headers=headers)

res = conn.getresponse()
row_data = res.read()

data = row_data.decode("utf-8")

with open ("data_log_tsla.txt", "w") as plik:
	print(data, file=plik)