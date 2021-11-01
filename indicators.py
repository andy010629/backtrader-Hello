import backtrader as bt
import datetime

class ud(bt.Indicator):
    lines = ('up','down','mid')


    plotlines = dict(
            mid=dict(ls='--'),  # dashed line
            # dch=dict(_samecolor=True),  # use same color as prev line (dcm)
            # dcl=dict(_samecolor=True),  # use same color as prev line (dch)
    )

    def __init__(self):
        self.addminperiod(1)
        self.plotinfo.plotmaster = self.data

    def next(self):

        # if self.data.datetime.time() == datetime.time(8,46) or (
        #     self.data.datetime.time() >= datetime.time()
        # ):
        #     self.up[0] = self.data.close[0]
        #     self.down[0] = self.data.close[0]

        if self.data.datetime.time() >= datetime.time(8,45) and  self.data.datetime.time() <= datetime.time(9, 15):
            self.up[0] = max(self.data.close[0], self.up[-1])
            self.down[0] = min(self.data.close[0],self.down[-1])    
            self.mid[0] = (self.up[0] + self.down[0])/2

        elif self.data.datetime.time() > datetime.time(9, 15) and self.data.datetime.time() <= datetime.time(13, 45):
            self.up[0] = self.up[-1]
            self.down[0] = self.down[-1]
            self.mid[0] = self.mid[-1]
            
        else:
            self.up[0] = self.data.close[0]
            self.down[0] = self.data.close[0]
            self.mid[0] = self.data.close[0]