from datetime import datetime

class BacktestingTrade():
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

class BacktestingResult():

    def __init__(self):
        self.trades = []
