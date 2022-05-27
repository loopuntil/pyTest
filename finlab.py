import matplotlib.pyplot as plt
from pandas_datareader import data as web  # pip install pandas_datareader
import pandas as pd
import ffn
import matplotlib
matplotlib.use('TkAgg')

'''
prices = ffn.get('2330.TW, 0050.TW')
print(prices.head())
#prices.plot()
#prices.rebase().plot()
#prices.to_drawdown_series().plot()
prices.plot_corr_heatmap()

stats = prices.calc_stats()
stats.display()
plt.show()
'''

#data = web.DataReader("^TWII", "yahoo", "2000-01-01", "2010-01-01")
#data = web.DataReader("^TWII", "yahoo", "2010-01-01", "2015-01-01")
#data = web.DataReader("^TWII", "yahoo", "2015-01-01")
#data = web.DataReader("^TWII", "yahoo", "2010-01-01")
data = web.DataReader("0050.TW", "yahoo", "2001-01-01")

# print(data)

c = data['Adj Close']['2015':]  # 還原除權息
#c = ffn.get('0050.TW')['0050tw']['2015':]

print(c)
c10 = c.rolling(10, min_periods=1).mean()
c20 = c.rolling(20, min_periods=1).mean()
c60 = c.rolling(60, min_periods=1).mean()
c120 = c.rolling(120, min_periods=1).mean()

signal0 = c > c60
signal1 = c > c20
signal2 = (((c < c60) & (c > c10)) | ((c > c60) & (c > c20)))

# signgal =

#(c.shift(-1) / c)[signal0].cumprod().plot(color='grey')
#(c.shift(-1) / c)[signal1].cumprod().plot(color='red')
(c.shift(-1) / c)[signal2].cumprod().plot(color='yellow')
(c.shift(-1) / c).cumprod().plot(color='blue')

# c['2010':].plot()
# c60['2010':].plot()
# c20['2015':].plot()
plt.show()
