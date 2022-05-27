import matplotlib.pyplot as plt
from pandas_datareader import data as web 
import pandas as pd
import ffn
import matplotlib

matplotlib.use('TkAgg')

data = web.DataReader("^TWII", "yahoo", "2000-01-01")
#data = web.DataReader("^TWII", "yahoo", "2010-01-01", "2015-01-01")
#data = web.DataReader("^TWII", "yahoo", "2015-01-01")
#data = web.DataReader("^TWII", "yahoo", "2010-01-01")
data = web.DataReader("0056.TW", "yahoo", "2001-01-01")

# print(data)

c = data['Adj Close']['2000':'2020']  #Adj Close 還原除權息

#print(c)

# rolling 是移動時間窗的概念。min_periods 最小觀測量，=1代表時間窗內至少要有一個值

c10max = c.rolling(10, min_periods=1).max()
c10min = c.rolling(10, min_periods=1).min()
c10 = c.rolling(10, min_periods=1).mean()
c20 = c.rolling(20, min_periods=1).mean()
c20max = c.rolling(20, min_periods=1).max()
c20min = c.rolling(20, min_periods=1).min()
c60 = c.rolling(60, min_periods=1).mean()
c120 = c.rolling(120, min_periods=1).mean()

signal0 = c > c60 # 價格大於60日移動平均
signal1 = c > c20
signal2 = (((c < c60) & (c > c10)) | ((c > c60) & (c > c20))) #想法，季線以下找反轉點，季線以上抱一個波段
signal3 =  c20 > c60

#如果還有其他策略的話
#singalX = 
#(c.shift(-1) / c)[signalX].cumprod().plot(color='purple')
# 顏色表 https://www.cnblogs.com/darkknightzh/p/6117528.html

#(c.shift(-1) / c)[signal3].cumprod().plot(color='green')
#(c.shift(-1) / c)[signal0].cumprod().plot(color='grey')
#(c.shift(-1) / c)[signal1].cumprod().plot(color='red')
#(c.shift(-1) / c)[signal2].cumprod().plot(color='yellow')
(c.shift(-1) / c).cumprod().plot(color='blue')

plt.show()

from talib import abstract
from pandas_datareader import data as web
from backtesting.test import SMA
from backtesting.lib import crossover, SignalStrategy
from backtesting import Backtest, Strategy
import pandas as pd
import matplotlib

data = web.DataReader("^TWII", "yahoo", "2000-01-01")
# data = web.DataReader("2330.TW", "yahoo", "2000-01-01")


class SmaCross(Strategy):
    def init(self):
        _close = self.data['Close']
        self.ma1 = self.I(SMA, _close, 20)
        self.ma2 = self.I(SMA, _close, 60)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


class SignalX(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        # self.I 只是用來幫忙畫出移動平均線，Series 是用來將數列序列化
        ma5 = pd.Series(self.I(SMA, c, 5))
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))

        #加上均線斜率判斷後績效大增
        mSignal = (ma10 > ma10.shift())
        #利用60ma當濾網，季線以下的買入條件是必須大於10ma
        buySignal0 = (c < ma60) & (c > ma10) & mSignal
        #60ma以上則大於ma20才進場
        buySignal1 = (c > ma60) & (c > ma20) & mSignal
        buyFlag = pd.Series(buySignal0 | buySignal1)

        #當買入條件失敗時賣出
        sellSignal0 = (c < ma60) & ((c < ma10) & mSignal)
        sellSignal1 = (c > ma60) & ((c < ma20) & mSignal)
        sellFlag = pd.Series(sellSignal0 | sellSignal1)
        # buy = (c > ma60) & (c < ma60.shift())
        # sell = (c < ma60) & (c > ma60.shift())
        buy = buyFlag & (buyFlag.shift() == False)
        sell = sellFlag & (sellFlag.shift() == False)

        signal = buy.copy()
        signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()


class SignalKD(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        _data = {
            'close': self.data['Close'].astype(float),
            'open': self.data['Open'].astype(float),
            'high': self.data['High'].astype(float),
            'low': self.data['Low'].astype(float),
            'volume': self.data['Volume'].astype(float),
        }

        k, d = abstract.STOCH(_data, fastk_period=9)
        buyFlag = pd.Series(k > d)
        buy = buyFlag & (buyFlag.shift() == False)
        sellFlag = pd.Series(k < d)
        sell = sellFlag & (sellFlag.shift() == False)
        signal = buy.copy()
        signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()


class SignalWeekKD(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        ma5 = pd.Series(self.I(SMA, c, 5))
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        _data = {
            'close': self.data['Close'].astype(float),
            'open': self.data['Open'].astype(float),
            'high': self.data['High'].astype(float),
            'low': self.data['Low'].astype(float),
            'volume': self.data['Volume'].astype(float),
        }

        k, d = abstract.STOCH(_data, fastk_period=45, slowk_period=15,slowd_period=15)
        buySignal0 = (d < 80)
        buySignal1 = (k> d)
        #加了斜率判斷後報酬率有提升約7%吧
        mSignal = (ma10 > ma10.shift())
        buyFlag = pd.Series(buySignal0 & buySignal1 & mSignal)
        buy = buyFlag & (buyFlag.shift() == False)
        sellSignal0 = (d > 80)
        sellSignal1 = (k < d)        
        sellFlag = pd.Series(sellSignal0 & sellSignal1 & (~mSignal))
        sell = sellFlag & (sellFlag.shift() == False)
        signal = buy.copy()
        signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()

class SignalMACD(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        _data = {
            'close': self.data['Close'].astype(float),
            'open': self.data['Open'].astype(float),
            'high': self.data['High'].astype(float),
            'low': self.data['Low'].astype(float),
            'volume': self.data['Volume'].astype(float),
        }

        macd, signal, hist = abstract.MACD(_data)
        buyFlag = pd.Series((macd > 0))
        buy = buyFlag & (buyFlag.shift() == False)
        sellFlag = pd.Series(macd < 0)
        sell = sellFlag & (sellFlag.shift() == False)
        signal = buy.copy()
        signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()
#注意！周層級的MACD最佳策略，"沒有"賣出！
class SignalWeekMACD(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        _data = {
            'close': self.data['Close'].astype(float),
            'open': self.data['Open'].astype(float),
            'high': self.data['High'].astype(float),
            'low': self.data['Low'].astype(float),
            'volume': self.data['Volume'].astype(float),
        }

        macd, signal, hist = abstract.MACD(_data,fastperiod = 12*5,slowperiod= 26*5,signalperiod= 9*5)
        #macd加入斜率判斷後績效反而會變差，就不列了
        macdSignal = (macd > 0)
        buyFlag = pd.Series(macdSignal)
        buy = buyFlag & (buyFlag.shift() == False)
        sellFlag = pd.Series(macd < 0)
        sell = sellFlag & (sellFlag.shift() == False)
        signal = buy.copy()
        #沒有賣出！加上去績效就不好了
        #signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()


'''
bt = Backtest(data['2015':], SignalX,
              cash=100000, commission=.001)
bt.run()
bt.plot()

btKD = Backtest(data['2015':], SignalWeekKD,
              cash=100000, commission=.001)
btKD.run()
btKD.plot()

btMACD = Backtest(data['2015':], SignalWeekMACD,
              cash=100000, commission=.001)

btMACD.run()
btMACD.plot()
'''