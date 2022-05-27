import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from talib import abstract
import sys

print("python版本:%s"% sys.version)

print(abstract.MACD )

dictionary = {'A':'an animal',
              'B':'a color',
              'C':'a fruit'}
dictionary = pd.Series(dictionary)
print(dictionary)



x = np.random.randn(2, 2)
print(x)
y = x + 1
print('************')
print(y)

x = np.random.randint(4, size=10)

print(x)

# 產生矩陣
#x = np.random.randn(5, 4)
# print(x)
# 平均值
print(x.mean())

# 標準差
print(x.std())


'''
years = [1950,1960,1965,1970,1975,1980,
        1985,1990,1995,2000,2005,
        2010,2015]
pops = [2.5,2.7,3,3.3,3.6,4.0,
        4.4,4.8,5.3,6.1,6.5,6.9,7.3]

deaths = [1.2,1.7,1.8,2.2,2.5,2.7,2.9,3,3.1,3.2,3.5,3.6,4]

lines = plt.plot(years, pops, years,deaths)
plt.setp(lines,marker = "o") # marker = "o"，設定點點的樣式。
plt.title("Population Growth") # title
plt.ylabel("Population in billions") # y label
plt.xlabel("Population growth by year") # x label
plt.grid(True)
plt.show()   
'''

'''
x = np.arange(0, 1.0, 0.01)
y1 = np.sin(4*np.pi*x)
y2 = np.sin(2*np.pi*x)
lines = plt.plot(x, y1, x, y2)
l1, l2 = lines
plt.setp(lines, linestyle='--')      
plt.show()    
'''

'''
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web
import datetime

start = datetime.datetime(2016, 1, 1)
end = datetime.datetime(2017, 1, 1)

data = web.DataReader("^twii", 'yahoo', start, end)
data.plot()
'''
