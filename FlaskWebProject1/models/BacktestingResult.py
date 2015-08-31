class BacktestingTrade(object):

    def __init__(self, buy_price, sell_price, buy_date, sell_date, cash, stocks, comment):
        self.buy_date = str(buy_date)
        self.buy_price = str(buy_price)
        self.sell_date = str(sell_date)
        self.sell_price = str(sell_price)
        self.cash = str(cash)
        self.profit = str((sell_price*stocks)-(buy_price*stocks))
        self.comment = comment

class BacktestingResult(object):
    def __init__(self):
        self.trades = []