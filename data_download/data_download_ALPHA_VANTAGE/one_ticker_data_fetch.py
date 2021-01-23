import pandas as pd
import openpyxl

from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='YCQCCO0INNSEDK0F')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL',interval='1min', outputsize='full')

df = pd.DataFrame.from_dict(data)
df_t = df.T

print(df_t)
print("KONIEC DANYCH. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print(meta_data)

df_t.to_excel("output_alpha_vantage.xlsx")

xfile = openpyxl.load_workbook('output_alpha_vantage.xlsx')

sheet = xfile.get_sheet_by_name('Sheet1')
sheet['H1'] = str(meta_data)
xfile.save('output_alpha_vantage.xlsx')
xfile.close()