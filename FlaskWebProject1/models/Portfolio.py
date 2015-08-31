from datetime import date, timedelta, datetime
import ystockquote as y
from decimal import *
import json as j
from FlaskWebProject1 import db

class Portfolio(db.Model):
    __tablename__ = "portfolio"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cash = db.Column(db.Integer)
    open_positions = db.relationship("Position", backref="open_positions", lazy='dynamic')
    closed_positions = db.relationship("Position", backref="closed_positions", lazy='dynamic')

    def __init__(self, name, start_cash):
        self.name = name
        self.open_positions = []
        self.closed_positions = []
        self.cash = int(start_cash)


    def buy(self, ticker, amount):
        buy_price = y.get_price(ticker)
        buy_date = datetime.today()
        pos = Position(ticker, buy_date, buy_price, amount)
        self.open_positions.append(pos)
        buy = Decimal(buy_price.strip(' "')) * Decimal(amount)
        self.cash = int(self.cash - buy)

    def sell(self, ticker):
        position = [i for i in self.open_positions if i.ticker == ticker][0]
        profit = position.sell()
        self.cash = int(self.cash + profit)
        self.open_positions.remove(position)
        self.closed_positions.append(position)

    def getportfoliovalue(self):
        value= self.cash
        for p in self.open_positions:
            p.profit = int(p.getprofit())
            p.current_price = p.getprice()
            profit = p.getvalue()
            value = Decimal(value + profit)
        self.value = int(value)

    def gethistory(self):
        return self.closed_positions

class Position(db.Model):
    __tablename__ = "position"
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(80))
    buy_date = db.Column(db.DateTime)
    buy_price = db.Column(db.String(120))
    sell_date = db.Column(db.DateTime)
    sell_price = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    portfolio = db.relationship('Portfolio')

    def __init__(self, ticker, buy_date, buy_price, amount):
        self.ticker = ticker
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.amount = amount
        self.sell_date = None
        self.sell_price = 0
        self.current_price = buy_price

    def getprofit(self):
        value = y.get_price(self.ticker)
        return (Decimal(value) - Decimal(self.buy_price)) * Decimal(self.amount)

    def getprice(self):
        price =  y.get_price(self.ticker)
        return Decimal(price)

    def getvalue(self):
        value = y.get_price(self.ticker)
        return Decimal(value) * Decimal(self.amount)

    def sell(self):
        self.sell_date = datetime.today()
        self.sell_price = y.get_price(self.ticker)
        return Decimal(self.sell_price) * Decimal(self.amount)