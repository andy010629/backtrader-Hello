'''
buy_bracket -> 打三單
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import pandas as pd
import datetime
from strategy import test

# create object
cerebro = bt.Cerebro()

# make data feeds
dataframe = pd.read_csv('2021TXF.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['Date']+' '+dataframe['Time'])
dataframe.set_index('datetime',inplace=True)
dataframe['openintrest'] = 0
TXF_his = bt.feeds.PandasData(dataname=dataframe,
        fromdate= datetime.datetime(2021,1,4),
        todate = datetime.datetime(2021,1,5),
        timeframe=bt.TimeFrame.Minutes
    )


cerebro.adddata(TXF_his)

# # TXF_his.volume.plot = False
# cerebro.datas[0].volume.plot = False

cerebro.broker.setcash(20000)

# # merge minK to HourK (會自動 feed 進 cerebro)
# cerebro.resampledata(TXF_his,  timeframe=bt.TimeFrame.Minutes, compression=60)
# cerebro.resampledata(TXF_his,  timeframe=bt.TimeFrame.Days)

# add strategy
cerebro.addstrategy(test)


# run app
cerebro.run(oldbuysell=True)

# plot
# cerebro.plot(volume=False)
cerebro.plot(style='candlestick', barup='green', bardown='red')