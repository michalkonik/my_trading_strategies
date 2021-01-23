import openpyxl
import json
import pandas as pd

with open ("data_log_tsla.txt") as f:
    content = f.read()

d = json.loads(content)

df = pd.json_normalize(d['stock'])
print(df)
df_t = df.T

df_t.to_excel("structured_data_tsla.xlsx")