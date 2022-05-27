# basic
import numpy as np
import pandas as pd
import matplotlib as mpl
from cycler import cycler
# get data
import pandas_datareader as data

# visual
import matplotlib.pyplot as plt
import mplfinance as mpf
import seaborn as sns

# time
import datetime as datetime

# talib
import talib

df = data.DataReader("0050.TW", "yahoo", "2019-01-01")

# figratio:圖形縱橫比
# figscale:圖形尺寸（越大越高）

kwargs = dict(
    type='candle',
    mav=(10, 20, 60),
    volume=True,
    title='\ncandle_line',
    ylabel='OHLC Candles',
    ylabel_lower='Shares\nTraded Volume',
    figratio=(15, 10),
    figscale=1)

# up:就是紅k
# down:黑k
# edge:(i表示繼承up和down
# wick:上下影線
# volume:成交量顏色
# inherit:是否繼承
mc = mpf.make_marketcolors(
    up='red',
    down='green',
    edge='i',
    wick='i',
    volume='in',
    inherit=True)

# 圖形風格
# gridaxis:網格現位置
# gridstyle:線型
# y_on_right:y軸位置是否在右
s = mpf.make_mpf_style(
    gridaxis='both',
    gridstyle='-.',
    y_on_right=False,
    marketcolors=mc)

# 均線顏色 可用默認
mpl.rcParams['axes.prop_cycle'] = cycler(
    color=['dodgerblue', 'deeppink',
           'navy', 'teal', 'maroon', 'darkorange',
           'indigo'])

# 線寬
mpl.rcParams['lines.linewidth'] = .5

mpf.plot(df[-180:],
         **kwargs,
         style=s)

# mpf.plot(df,type='candle',mav=(10,20,60),volume=True)
plt.show()
