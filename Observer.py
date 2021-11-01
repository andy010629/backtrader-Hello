import backtrader as bt
class Value(bt.Observer):

    _stclock = True

    params = (
        ('fund', None),
    )

    lines = ('value',)

    plotinfo = dict(plot=True, subplot=True)

    def start(self):
        # if self.p.fund is None:
        #     self._fundmode = self._owner.broker.fundmode
        # else:
        #     self._fundmode = self.p.fund
        self._fundmode = 0
        self.startCash =  self._owner.broker.getvalue()

    def next(self):
        if not self._fundmode:
            self.lines[0][0] = self._owner.broker.getvalue() -  self.startCash
        else:
            self.lines[0][0] = self._owner.broker.fundvalue



class Broker(bt.Observer):
    '''This observer keeps track of the current cash amount and portfolio value in
    the broker (including the cash)

    Params: None
    '''
    _stclock = True

    params = (
        ('fund', None),
    )

    alias = ('CashValue',)
    lines = ('cash', 'value')

    plotinfo = dict(plot=False, subplot=True)

    def start(self):
        if self.p.fund is None:
            self._fundmode = self._owner.broker.fundmode
        else:
            self._fundmode = self.p.fund

        if self._fundmode:
            self.plotlines.cash._plotskip = True
            self.plotlines.value._name = 'FundValue'

    def next(self):
        if not self._fundmode:
            self.lines.value[0] = value = self._owner.broker.getvalue()
            self.lines.cash[0] = self._owner.broker.getcash()
        else:
            self.lines.value[0] = self._owner.broker.fundvalue


