import backtrader as bt
from indicators import ud
import datetime
from mongo import mongo_to_dataframe
from compute import getSymbolName,getMiddleLine

class myORB(bt.Strategy):

    def __init__(self):
        self.up_down = ud(self.data)

        self.buycon = bt.indicators.CrossOver(
            self.data.close, self.up_down.up)

        self.sellcon = bt.indicators.CrossDown(
            self.data.close, self.up_down.down)

        # self.optval = 

        self.buycon.plotinfo.plot = False
        self.sellcon.plotinfo.plot = False
    
    def next(self):

        ### Futures ###
        if self.data.datetime.time() > datetime.time(9, 15) and self.data.datetime.time() < datetime.time(13, 30) and not self.position:
            curPrice = self.data.close[0]
            midPrice = (self.up_down.up[0]+self.up_down.down[0])/2
            if self.buycon[0] == 1:
                self.order =  self.buy_bracket(limitprice=curPrice*3-midPrice*2, price=curPrice, stopprice=midPrice)
            elif self.sellcon[0] == 1:
                self.order = self.sell_bracket(limitprice=curPrice*3-midPrice*2, price=curPrice, stopprice=midPrice)
           
        if  self.position and self.data.datetime.time() == datetime.time(13, 30):
            for o in self.order: 
                self.cancel(o)
            self.order = self.close()
        # if self.data.datetime.time() == datetime.time(9,00):

        ### Options ###
        if self.data.datetime.time() > datetime.time(9, 15) and self.data.datetime.time() < datetime.time(13, 30) and not self.position:
            upStrike = getMiddleLine({'up':self.up_down.up[0]})
            downStrike = getMiddleLine({'down':self.up_down.down[0]})
            upSymbol = (getSymbolName(upStrike,'call',self.data.datetime.datetime()))
            downSymbol = (getSymbolName(downStrike,'put',self.data.datetime.datetime()))
            callprice = mongo_to_dataframe(upSymbol,self.data.datetime.datetime())['Close']
            putprice = (mongo_to_dataframe(downSymbol,self.data.datetime.datetime())['Close'])

            if self.buycon[0] == 1:
                print('Buy',callprice)
            elif self.sellcon[0] == 1:
                print('Sell',putprice)

            # self.test.append((callprice,putprice))



class ChinaORB(bt.Strategy):
    
    def __init__(self):
        self.up_down = ud(self.data)
        
        self.buycon = bt.indicators.CrossOver(
            self.data.close, self.up_down.up)
        self.sellcon = bt.indicators.CrossDown(
            self.data.close, self.up_down.down)

        self.buycon.plotinfo.plot = False
        self.sellcon.plotinfo.plot = False
        self.bought_today = False

    def next(self):

        ### Futures ###
        if not self.bought_today and not self.position and self.data.datetime.time() > datetime.time(9, 15) and self.data.datetime.time() < datetime.time(13, 30):
            curPrice = self.data.close[0]
            midPrice = (self.up_down.up[0]+self.up_down.down[0])/2
            if self.buycon[0] == 1:
                self.order =  self.buy_bracket(limitprice=curPrice*3-midPrice*2, price=curPrice, stopprice=midPrice)
            elif self.sellcon[0] == 1:
                self.order = self.sell_bracket(limitprice=curPrice*3-midPrice*2, price=curPrice, stopprice=midPrice)
           
        if  self.position and self.data.datetime.time() == datetime.time(13, 30):
            for o in self.order: 
                self.cancel(o)
            self.order = self.close()
        # if self.data.datetime.time() == datetime.time(9,00):
