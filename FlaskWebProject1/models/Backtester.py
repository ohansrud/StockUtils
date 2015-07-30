from datetime import date, timedelta, datetime
from FlaskWebProject1.models.StockQuote import StockQuote as st
from FlaskWebProject1.models.BacktestingResult import *
import math
import sys
from pprint import pprint

class Backtester(object):
    def __init__(self, buy_signal, sell_signal, item):
        self.result = BacktestingResult()
        self.today = datetime.today()
        self.day = timedelta(days=1)
        self.year = timedelta(days=(365*2))
        self.start = self.today-self.year
        self.end = self.today-self.day
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal
        self.item = item

        try:
            self.s = st(item, str(self.start.strftime('%Y-%m-%d')), str(self.end.strftime('%Y-%m-%d')))
        except:
            print("Import Error")

    def start(self):
        return self.start

    def backtest(self):
        i = 0
        cash=10000
        while i < len(self.s.df):
            try:
                #Look for bBuy Signal
                if self.s.df[self.buy_signal][i] == 1:
                    buy_date = self.s.df.index[i]
                    #Kjøp
                    buy_price = self.s.df['close'][i]

                    stocks = math.floor(cash / buy_price)
                    cash = cash%buy_price
                    print(buy_date)
                    print("Buy: " + str(buy_price))
                    #Cannot buy and sell on the same day. Skips to next day to look for exit.
                    i= i+1
                    #Look for exit signal
                    while i < len(self.s.df):
                        #Set stop loss and take profit +- 5 * atr of previous day
                        atr = self.s.atr[i-1]
                        stop_loss = self.s.df['close'][i-1] - atr * 5
                        take_profit = self.s.df['close'][i-1] + atr* 5

                        #Look for stop loss
                        if self.s.df['close'][i] < stop_loss or self.s.df['low'][i] < stop_loss:
                            sell_price = stop_loss
                            print("Stop loss!")
                            break

                        #Look for take profit
                        elif self.s.df['close'][i] > take_profit or self.s.df['high'][i] > take_profit:
                            sell_price = take_profit
                            print("Take profit!")
                            break

                        #Look for sell signal
                        elif self.s.df[self.sell_signal][i] == 1:
                            print("Exit signal!")
                            sell_price = self.s.df['close'][i]
                            break

                        #Look for last day
                        elif i == len(self.s.df)-1:
                            print("End of sequence")
                            sell_price = self.s.df['close'][i]
                            break
                        else:
                            i=i+1

                    sell_date = self.s.df.index[i]
                    cash = cash + (sell_price*stocks)
                    self.result.trades.append(BacktestingTrade(buy_price, sell_price, buy_date, sell_date, cash, stocks).serialize)
                    print(self.s.df.index[i])
                    print("Sell: " + str(sell_price))
                    print("Profit: " + str((sell_price*stocks)-(buy_price*stocks)))
                    stocks = 0
                    print("Cash: " + str(cash))
                    print(" --------- ")

                    #Hvis det ikke er mer penger igjen
                    if(cash<=0):
                        print("No funds!")
                        break
                i=i+1
            except:
                error = sys.exc_info()
                pprint(error)
                i=i+1
        #Selg aksjer hvis det er noe igjen
        if stocks > 0:
            sell_price = self.s.df['close'][i-1]
            cash = cash + (sell_price*stocks)

            print(self.s.df.index[i-1])
            self.result.trades.append(BacktestingTrade(buy_price, sell_price, buy_date, sell_date, cash, stocks))
            print("Sell: " + str(sell_price))
            print("Profit: " + str((sell_price*stocks)-(buy_price*stocks)))
            stocks = 0
            print("Cash: " + str(cash))
            print(" --------- ")
        #return result

class Backtester_DoubleCross(Backtester):
    def __init__(self, item):
        self.buy_signal = 'doublecross'
        self.sell_signal = 'slowk_drops_under_80'
        Backtester.__init__(self, self.buy_signal, self.sell_signal, item)

        cash = 10000
        stocks = 0

        self.s.stoch_crossover()
        self.s.macd_crossover()
        self.s.doublecross()
        self.s.slowk_drops_under_80()
        self.backtest()

class Backtester_RSI(Backtester):
    def __init__(self, item):
        self.buy_signal = 'rsi_over_70'
        self.sell_signal = 'rsi_under_50'
        Backtester.__init__(self, self.buy_signal, self.sell_signal, item)

        cash = 10000
        stocks = 0

        self.s.scan_rsi_over_70()
        self.s.scan_rsi_under_50()
        self.backtest()