from datetime import date, timedelta, datetime
import ystockquote as y
from decimal import *

class Portfolio(object):
    def __init__(self, start_cash):
        self.open_positions = []
        self.closed_positions = []
        self.cash = start_cash

    def buy(self, ticker, amount):
        buy_price = y.get_price(ticker)
        buy_date = datetime.today()
        pos = Position(ticker, buy_date, buy_price, amount)
        self.open_positions.append(pos)

        self.cash = self.cash - (Decimal(buy_price) * amount)

    def sell(self, ticker):
        position = [i for i in self.open_positions if i.ticker == ticker][0]
        profit = position.sell()
        self.cash = self.cash + profit
        self.open_positions.remove(position)
        self.closed_positions.append(position)

    def getportfoliovalue(self):
        value= self.cash
        for p in self.open_positions:
            value = value + p.getprofit()

    def gethistory(self):
        return self.closed_positions


class Position(object):
    def __init__(self, ticker, buy_date, buy_price, amount):
        self.ticker = ticker
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.amount = amount

    def getprofit(self):
        value = y.get_price(self.ticker)
        return Decimal(value) - Decimal(self.buy_price)

    def sell(self):
        self.sell_date = datetime.today()
        self.sell_price = y.get_price(self.ticker)
        return Decimal(self.sell_price) * self.amount







