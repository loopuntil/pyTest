from talib import abstract
from pandas_datareader import data as web
from backtesting.test import SMA
from backtesting.lib import crossover, SignalStrategy
from backtesting import Backtest, Strategy
import pandas as pd
import matplotlib
import datetime

dataTWII = web.DataReader("^TWII", "yahoo", "2000-01-01")
data = web.DataReader("0050.TW", "yahoo", "2000-01-01")



'''
#失敗的策略先註解起來

class SignalX(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        # self.I 只是用來幫忙畫出移動平均線，Series 是用來將數列序列化
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
        #signal[sell] = -1
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
            'close': self.data['Close'].astype(float),
            'open': self.data['Open'].astype(float),
            'high': self.data['High'].astype(float),
            'low': self.data['Low'].astype(float),
            'volume': self.data['Volume'].astype(float),
        }

        k, d = abstract.STOCH(_data, fastk_period=9)
        buySignal = (d<20) & (k>d)
        buyFlag = pd.Series(buySignal)
        buy = buyFlag & (buyFlag.shift() == False)
        sellSignal = (d > 80) & (k < d)
        sellFlag = pd.Series(sellSignal)
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
'''

# 定期定額購買0050 (Dollar Cost Averaging)


class SignalDCA(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        # self.I 只是用來幫忙畫出移動平均線，Series 是用來將數列序列化
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

        # 40或60皆可
        buySignal0 = c.index % 60 == 0
        buyFlag = pd.Series(buySignal0)

        #sellSignal0 = 不需要賣出策略
        #sellFlag = pd.Series(sellSignal0)

        buy = buyFlag & (buyFlag.shift() == False)
        #sell = sellFlag & (sellFlag.shift() == False)

        signal = buy.copy()
        #signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()

# 當大盤周macd轉正，買進0050


class SignalWeekMACD(SignalStrategy):
    def init(self):
        super().init()
        c = pd.Series(self.data['Close'])
        ma10 = pd.Series(self.I(SMA, c, 10))
        ma20 = pd.Series(self.I(SMA, c, 20))
        ma60 = pd.Series(self.I(SMA, c, 60))
        # 這邊取巧加權指數直接抓全域變數的值，不再多傳一個參數
        _index = str(self.data.index[0])
        _dataTWII = dataTWII[_index:]
        _data = {
            'close': _dataTWII['Close'].astype(float),
            'open': _dataTWII['Open'].astype(float),
            'high': _dataTWII['High'].astype(float),
            'low': _dataTWII['Low'].astype(float),
            'volume': _dataTWII['Volume'].astype(float),
        }

        macd, signal, hist = abstract.MACD(
            _data, fastperiod=12*5, slowperiod=26*5, signalperiod=9*5)
        # macd加入斜率判斷後績效反而會變差，就不列了
        macdSignal = (macd > 0)
        buyFlag = pd.Series(macdSignal)
        buy = buyFlag & (buyFlag.shift() == False)
        sellFlag = pd.Series(macd < 0)
        sell = sellFlag & (sellFlag.shift() == False)
        signal = buy.copy()
        # 沒有賣出！加上去績效就不好了
        #signal[sell] = -1
        self.set_signal(signal)

    def next(self):
        super().next()


bt = Backtest(data['2015':], SignalDCA, cash=100000, commission=.002)

bt.run()
bt.plot()

bt1 = Backtest(data['2015':], SignalWeekMACD, cash=100000, commission=.002)

bt1.run()
bt1.plot()
