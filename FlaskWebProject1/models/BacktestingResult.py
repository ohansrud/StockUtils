from datetime import datetime, date

class BacktestingTrade(object):
     #buy_date = datetime
    #sell_date = ""
    #buy_price = 0
    #sell_price = 0
    #cash = 0

    def __init__(self, buy_price, sell_price, buy_date, sell_date, cash, stocks):
        self.buy_date = str(buy_date)
        self.buy_price = str(buy_price)
        self.sell_date = str(sell_date)
        self.sell_price = str(sell_price)
        self.cash = str(cash)
        self.profit = str((sell_price*stocks)-(buy_price*stocks))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'buy_date'         : self.buy_date,
           'buy_price'         : self.buy_price,
           'sell_date'         : self.sell_date,
           'sell_price'         : self.sell_price,
           'cash'         : self.cash,
           'profit'         : self.profit,
       }

class BacktestingResult(object):
    def __init__(self):
        self.trades = []

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'trades'         : self.trades
       }