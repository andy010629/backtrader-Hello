import backtrader as bt
from indicators import ud
import datetime


class ORB(bt.Strategy):

    def __init__(self):
        self.up_down = ud(self.data)

        self.buycon = bt.indicators.CrossOver(
            self.data.close, self.up_down.up)

        self.sellcon = bt.indicators.CrossDown(
            self.data.close, self.up_down.down)

        self.buycon.plotinfo.plot = False
        self.sellcon.plotinfo.plot = False

    def next(self):

        if not self.position:
            curPrice = self.data.close[0]
            midPrice = (self.up_down.up[0]+self.up_down.down[0])/2
            if self.buycon[0] == 1:
                self.order =  self.buy_bracket(limitprice=curPrice*3-midPrice*2, price=curPrice, stopprice=midPrice)
            elif self.sellcon[0] == 1:
                self.order = self.sell_bracket(limitprice=curPrice*3-midPrice*2, price=curPrice, stopprice=midPrice)
   


        if self.data.datetime.time() == datetime.time(13, 30):
            self.order = self.close()
