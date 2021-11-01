import backtrader as bt
import datetime

class ud(bt.Indicator):
    lines = ('up','down','mid')
    plotlines = dict(
            mid=dict(ls='--'),  # dashed line
    )

    def __init__(self):
        self.addminperiod(1)
        self.plotinfo.plotmaster = self.data

    def next(self):

        opening_range_start_time =  datetime.time(9,30)
        opening_range_end_time = datetime.time(9, 45)
        market_close_time = datetime.time(13, 45)



        if self.data.datetime.time() >= opening_range_start_time and  self.data.datetime.time() <= opening_range_end_time:
            self.up[0] = max(self.data.high[0], self.up[-1])
            self.down[0] = min(self.data.low[0],self.down[-1])    
            self.mid[0] = (self.up[0] + self.down[0])/2

        elif self.data.datetime.time() > opening_range_end_time and self.data.datetime.time() <= market_close_time:
            self.up[0] = self.up[-1]
            self.down[0] = self.down[-1]
            self.mid[0] = self.mid[-1]
        else:
            self.up[0] = self.data.open[0]
            self.down[0] = self.data.low[0]
            self.mid[0] = (self.data.open[0] + self.data.low[0]) /2