import pandas as pd
import datetime
import json
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR 
import numpy as np
import matplotlib.pyplot as plt

with open("ibm_ytd.json","r") as fp:
    json_d = json.load(fp)

#load the saved JSON response in Pandas DataFrame.
ticks_d = json_d['result']['IBM:US']['ticks']
df = pd.DataFrame(ticks_d)
df['Close'] = df['close']
df['Date'] = df['time'].apply(lambda x:datetime.datetime.fromtimestamp(x))
df = df.set_index('time')
data = df.sort_index(ascending=True, axis=0)
print(data)

#creating a separate dataset
new_data = data[['Date','Close']]
index = range(0,len(new_data))
new_data['index']=index
new_data=new_data.set_index('index')
new_data['Date'] = pd.to_datetime(new_data.Date,format='%Y-%m-%d')
print(new_data)

def adddatepart(data,col):
    data['month'] = data[col].dt.month
    data['day'] = data[col].dt.day
    data['year'] = data[col].dt.year
    data['quarter'] = data[col].dt.quarter
    data['dayofweek'] = data[col].dt.dayofweek
    data['dayofyear'] = data[col].dt.dayofyear
    #data['dayinmonth'] = data[col].dt.daysinmonth
    data['is_month_end'] = data[col].dt.is_month_end.astype(int)
    data['is_month_start'] = data[col].dt.is_month_start.astype(int)
    data['is_quarter_start'] = data[col].dt.is_quarter_start.astype(int)
    data['is_quarter_end'] = data[col].dt.is_quarter_end.astype(int)
    data['is_year_start'] = data[col].dt.is_year_start.astype(int)
    data['is_year_end'] = data[col].dt.is_year_end.astype(int)
    data['mon_fri'] = data['dayofweek'].apply(lambda x: 1 if x==0 or x==4 else 0)
    return data
    
adddatepart(new_data,'Date')
print(new_data)

X = new_data.drop('Date',axis=1)
X.drop('Close',axis=1,inplace=True)
print(X)

Y = new_data['Close']
print(Y)

train_pct_index = int(0.7 * len(X))
x_train, x_validate = X[:train_pct_index], X[train_pct_index:]
y_train, y_validate = Y[:train_pct_index], Y[train_pct_index:]

model = LinearRegression()
model.fit(x_train,y_train)

#make predictions and find the rmse
preds = model.predict(x_validate)
rms=np.sqrt(np.mean(np.power((np.array(y_validate)-np.array(preds)),2)))
# This gives the accuracy of the model, the lesser the better
print("Rms linear reg",rms)

viz_data = new_data[['Date','Close']]
viz_data['Predictions'] = 0
for i in range(train_pct_index,len(viz_data)):
    viz_data.loc[i,'Predictions'] = preds[i-train_pct_index]
print(viz_data)

fig= plt.figure(figsize=(20,10))
dates = viz_data['Date'][train_pct_index:]
plt.plot(dates, viz_data['Close'][train_pct_index:], c='k', label='Actual Data')
plt.plot(dates, preds, c='g', label='Linear model')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Linear Regression of Stock Prediction')
plt.grid()
plt.legend()
plt.show()