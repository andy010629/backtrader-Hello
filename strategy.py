import backtrader as bt
from indicators import ud
import datetime

class test(bt.Strategy):

    def __init__(self):
        self.up_down = ud(self.data)

        self.buycon = bt.indicators.CrossOver(
            self.data.close, self.up_down.up)

        self.sellcon = bt.indicators.CrossDown(
            self.data.close, self.up_down.down)

        self.buycon.plotinfo.plot = False
        self.sellcon.plotinfo.plot = False

    def next(self):

        if not self.position and self.buycon[0] == 1:
            self.order = self.buy()
            # print(self.data.datetime.time())

        # if self.position == 1 and self.close

        # if self.sellcon[0]:
        #     self.order = self.sell()

        if self.data.datetime.time() == datetime.time(13, 30):
            self.order = self.close()
