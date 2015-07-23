from datetime import date, timedelta, datetime
from FlaskWebProject1.models.StockQuote import StockQuote as st

import ystockquote as y

def backtester_doublecross(item):
    profit = []
    print(item)
    today = datetime.today()
    day = timedelta(days=1)
    year = timedelta(days=(365*2))
    start = today-year
    end = today-day

    try:
        s = st(item, str(start.strftime('%Y-%m-%d')), str(end.strftime('%Y-%m-%d')))
    except:
        print("Import Error")
    #s = None

    cash = 10000
    stocks = 0   
        
    cash = s.backtest_doublecross(cash)
    print("Cash: " + str(cash) + ". Profit: " + str(cash-10000))
    profit.append(item + ": " + str(cash-10000))
    print("---------------------------------------")

    return profit

def backtester_rsi(item):
    profit = []
    print(item)
    today = datetime.today()
    day = timedelta(days=1)
    year = timedelta(days=(365*2))
    start = today-year
    end = today-day

    try:
        s = st(item, str(start.strftime('%Y-%m-%d')), str(end.strftime('%Y-%m-%d')))
    except:
        print("Import Error")
    #s = None

    cash = 10000
    stocks = 0   
        
    cash = s.backtest_rsi(cash)
    print("Cash: " + str(cash) + ". Profit: " + str(cash-10000))
    profit.append(item + ": " + str(cash-10000))
    print("---------------------------------------")

    return profit