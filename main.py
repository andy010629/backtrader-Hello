from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import pandas as pd
import datetime
from Strategys import ChinaORB
import Observer

# create objectG
cerebro = bt.Cerebro(stdstats=False)

# make data feeds
dataframe = pd.read_csv('2021TXF.csv')
dataframe['datetime'] = pd.to_datetime(dataframe['Date']+' '+dataframe['Time'])
dataframe.set_index('datetime',inplace=True)
dataframe['openintrest'] = 0


fromdate = datetime.datetime(2021,1,1)
todate = datetime.datetime(2021,1,31)

TXF_his = bt.feeds.PandasData(dataname=dataframe,
        fromdate= fromdate,
        todate = todate,
        timeframe=bt.TimeFrame.Minutes
    )


# cerebro.adddata(TXF_his)

# # TXF_his.volume.plot = False
# cerebro.datas[0].volume.plot = False

cerebro.broker.setcash(100000)

# # merge minK to HourK (會自動 feed 進 cerebro)
cerebro.resampledata(TXF_his,  timeframe=bt.TimeFrame.Minutes, compression=5)
# cerebro.resampledata(TXF_his,  timeframe=bt.TimeFrame.Days)

# add strategy
cerebro.addstrategy(ChinaORB)



# add observer
cerebro.addobserver(Observer.Value)
cerebro.addobserver(bt.observers.Trades)
cerebro.addobserver(bt.observers.BuySell)
cerebro.addobserver(Observer.Broker)




# add analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SR', timeframe=bt.TimeFrame.Days)

# add writer
cerebro.addwriter(bt.WriterFile, csv=True,out='result.csv')


# run backtrader
result = cerebro.run(oldbuysell=True)

# plot
cerebro.plot(style='candlestick', barup='green', bardown='red', volume=False)
# cerebro.plot(volume=False)


