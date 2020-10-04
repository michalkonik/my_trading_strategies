import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime,date

df = pd.read_excel('AAL\AAL.xlsx')
df = df.head(30)

print(df)

fig, ax = plt.subplots(figsize=(10, 7))

ax.plot(df.index, df["Open"], marker='v', linestyle='--', color='green')
ax.plot(df.index, df["Close"], marker='v', linestyle='--', color='blue')

ax.set_xlabel("when exactly")
ax.set_ylabel("price")
ax.set_title("what happens after 15% drop")

plt.xticks(df.index, df['Date'].astype(str), rotation=20)
ax.xaxis.set_major_locator(ticker.MultipleLocator(7))

#plt.show()
plt.savefig('foo.png')
plt.savefig('foo.pdf')