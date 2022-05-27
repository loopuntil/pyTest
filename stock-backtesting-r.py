from talib import abstract
from pandas_datareader import data as web
from backtesting.test import SMA
from backtesting.lib import crossover, SignalStrategy
from backtesting import Backtest, Strategy
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')

#data = web.DataReader("^TWII", "yahoo", "2000-01-01")
data = web.DataReader("2330.TW", "yahoo", "2000-01-01")


class SmaCross(Strategy):
    def init(self):
        _close = self.data['Adj Close']
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
        c = pd.Series(self.data['Adj Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        buyFlag = pd.Series(((c < ma60) & (c > ma10)) |
                            ((c > ma60) & (c > ma20)))

        sellFlag = pd.Series(((c < ma60) & (c < ma10)) |
                            ((c > ma60) & (c < ma20)))
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
        c = pd.Series(self.data['Adj Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        _data = {
            'close': self.data['Adj Close'].astype(float),
            'open': self.data['Open'].astype(float),
            'high': self.data['High'].astype(float),
            'low': self.data['Low'].astype(float),
            'volume': self.data['Volume'].astype(float),
        }

        k, d = abstract.STOCH(_data)
        buyFlag = pd.Series(k > d)
        buy = buyFlag & (buyFlag.shift() == False)
        sellFlag = pd.Series(k < d)
        sell = sellFlag & (sellFlag.shift() == False)
        signal = buy.copy()
        signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()


class SignalMACD(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Adj Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        _data = {
            'close': self.data['Adj Close'].astype(float),
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



print('*****')
print(str(data['2015':].index[0]))
'''
bt = Backtest(data['2015':], SignalX,
              cash=100000, commission=.001)

bt.run()
bt.plot()
'''