import matplotlib.pyplot as plt
from pandas_datareader import data as web  # pip install pandas_datareader
import pandas as pd
import ffn
import matplotlib
matplotlib.use('TkAgg')

data = web.DataReader("^TWII", "yahoo", "2000-01-01")
#data = web.DataReader("^TWII", "yahoo", "2010-01-01", "2015-01-01")
#data = web.DataReader("^TWII", "yahoo", "2015-01-01")
#data = web.DataReader("^TWII", "yahoo", "2010-01-01")
#data = web.DataReader("0050.TW", "yahoo", "2001-01-01")

# print(data)

c = data['Adj Close']['2015':'2020']  # 還原除權息

print(c)

c10max = c.rolling(10, min_periods=1).max()
c10min = c.rolling(10, min_periods=1).min()
c10 = c.rolling(10, min_periods=1).mean()
c20 = c.rolling(20, min_periods=1).mean()
c20max = c.rolling(20, min_periods=1).max()
c20min = c.rolling(20, min_periods=1).min()
c60 = c.rolling(60, min_periods=1).mean()
c120 = c.rolling(120, min_periods=1).mean()

signal0 = c > c60
signal1 = c > c20
signal2 = (((c < c60) & (c > c10)) | ((c > c60) & (c > c20))) #想法，季線以下找反轉點，季線以上抱一個波段
signal3 =  c20 > c60

#如果還有其他策略的話
#singalX = 
#(c.shift(-1) / c)[signalX].cumprod().plot(color='')

(c.shift(-1) / c)[signal3].cumprod().plot(color='green')
(c.shift(-1) / c)[signal0].cumprod().plot(color='grey')
(c.shift(-1) / c)[signal1].cumprod().plot(color='red')
(c.shift(-1) / c)[signal2].cumprod().plot(color='yellow')
(c.shift(-1) / c).cumprod().plot(color='blue')



plt.show()
