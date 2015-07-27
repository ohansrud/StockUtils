import numpy as np
from talib import abstract
import ystockquote as y
import pandas as pd
from pprint import pprint
from datetime import date, timedelta
import math
import sys
from FlaskWebProject1.models.BacktestingResult import BacktestingTrade, BacktestingResult

class StockQuote(object):
    """description of class"""
    sma = []
    stoch = []
    macd = []
    atr = []
    obv = []
    rsi = []
    df = []
    #wma = []

    def __init__(self, ticker, start, end):

        i = y.get_historical_prices(ticker, start, end)

        #Lag Pandas DataFrame
        df = pd.DataFrame(i)

        #Snu Dataframe
        df2 = df.transpose()

        #endre datatype til float
        df2 = df2.astype(float)
        df2 = df2.rename(columns={'Close': 'close', 'High': 'high', 'Open': 'open', 'Low': 'low','Volume': 'volume'})

        self.stoch = abstract.STOCH(df2, 14, 3)
        self.macd = abstract.MACD(df2)
        self.atr = abstract.ATR(df2)
        self.obv = abstract.OBV(df2) 
        self.rsi = abstract.RSI(df2)
        #self.wma = abstract.WMA(df2, 233)
        

        #kombinerer to dataframes
        self.df = pd.merge(df2, pd.DataFrame(self.macd), left_index=True, right_index=True, how='outer')

        self.df = pd.merge(self.df, self.stoch, left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.atr), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.obv), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.rsi), left_index=True, right_index=True, how='outer')
        #self.df = pd.merge(self.df, pd.DataFrame(self.wma), left_index=True, right_index=True, how='outer')
    
    #Scanner etter tilfeller der Slow K krysser med Slow D
    def stoch_crossover(self):
        self.df["array_K_cross_down"] = 0
        self.df["array_D_cross_down"] = 0
        i=0
        try:
            for i in range(0, len(self.df)):            
                try:
                    #raise RuntimeError
                    k = self.df.iloc[i-1]['slowk']
                    k2 = self.df.iloc[i]['slowk']
                    d = self.df.iloc[i-1]['slowd']
                    d2 = self.df.iloc[i]['slowd']
    
                    #k krysser under d
                    if k > d and k2 < d2:
                        self.df['array_K_cross_down'][i] = 1
                    else:
                        #d krysser under k
                        if k < d and k2 > d2:
                            self.df['array_D_cross_down'][i] = 1
                except:
                    print(sys.exc_info())
                    
        except:
            print(sys.exc_info())
        return self.df

    #Scanner etter tilfeller der macd krysser med signallinjen
    def macd_crossover(self):
        self.df["macd_cross_down"] = 0
        self.df["signal_cross_down"] = 0

        for i in range(0, len(self.df)):            
            try:
                m = self.df.iloc[i-1]['macd']
                m2 = self.df.iloc[i]['macd']
                s = self.df.iloc[i-1]['macdsignal']
                s2 = self.df.iloc[i]['macdsignal']
    
                #k krysser under d
                if m > s and m2 < s2:
                    self.df['macd_cross_down'][i] = 1
                else:
                    #d krysser under k
                    if m < s and m2 > s2:
                        self.df['signal_cross_down'][i] = 1
            except:
                pass

        return self.df
    
    #Scanner etter tilfeller der macd_crossover skjer 1-4 dager etter 
    #stochastic crossover
    def doublecross(self):
        self.df["doublecross"] = 0

        for i in range(0, len(self.df)):            
            try:
                d = self.df.iloc[i-4]['array_D_cross_down']
                s = self.df.iloc[i-4]['signal_cross_down']
                s2 = self.df.iloc[i-3]['signal_cross_down']
                s3 = self.df.iloc[i-2]['signal_cross_down']
                s4 = self.df.iloc[i-1]['signal_cross_down']
                s5 = self.df.iloc[i]['signal_cross_down']
    
                #k krysser under d
                if d == 1:
                    if s == 1 or s2 == 1 or s3 == 1 or s4 == 1 or s5 == 1:
                        self.df['doublecross'][i-4] = 1
            except:
                pass

        return self.df

    def slowk_drops_under_80(self):
        self.df["slowk_drops_under_80"] = 0
        for i in range(0, len(self.df)):            
            try:
                slowk = self.df.iloc[i]['slowk']
                slowk2 = self.df.iloc[i+1]['slowk']
    
                #k krysser under 80
                if slowk > 80 and slowk2 < 80:
                    self.df['slowk_drops_under_80'][i] = 1
                    a = self.df.index[i]
            except:
                pass
        return self.df

    def turning_points(self):
        self.df["max"] = 0
        self.df["min"] = 0
        for i in range(0, len(self.df)):
            try:
                o = self.df.iloc[i]['open']
                h = self.df.iloc[i]['high']
                l = self.df.iloc[i]['low']
                c = self.df.iloc[i]['close']
                self.df['max'][i] = max([o,h,c])
                self.df['min'][i] = min([o,l,c])
            except:
                pass
        return None

    def backtest_doublecross(self, cash):
        result = BacktestingResult()
        self.stoch_crossover()
        self.macd_crossover()
        self.doublecross()
        self.slowk_drops_under_80()

        i = 0
        print(len(self.df))
        while i < len(self.df):
        #for i in range(0, len(self.df)):            
            try:
                if self.df['doublecross'][i] == 1:
                    buy_date = self.df.index[i]
                    #Kjøp
                    buy_price = self.df['close'][i]
                    #a = self.atr[i]
                    #stop_loss = buy_price - a*3

                    stocks = math.floor(cash / buy_price)
                    cash = cash%buy_price
                    print(self.df.index[i])
                    print("Buy: " + str(buy_price))
                    
                    a = i
                    while self.df['slowk_drops_under_80'][a] == 0:
                       if a== len(self.df):
                           sell_date = self.df.index[a]
                           break
                       a = a+1
                    i=a
                    sell_date = self.df.index[a-1]
                    #while self.df['close'][i] > stop_loss or self.df['slowk_drops_under_80'][i] == 0:
                     #   i = i+1  
                    #Selg Aksjer
                    sell_price = self.df['close'][i]
                    cash = cash + (sell_price*stocks)
                    result.trades.append(BacktestingTrade(buy_price, sell_price, buy_date, sell_date, cash, stocks))
                    print(self.df.index[i])
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
                print(sys.exc_info()[0])
                i=i+1
        #Selg aksjer hvis det er noe igjen
        if stocks > 0:
            sell_price = self.df['close'][i-1]
            cash = cash + (sell_price*stocks)
                    
            print(self.df.index[i-1])
            result.trades.append(BacktestingTrade(buy_price, sell_price, buy_date, sell_date, cash, stocks))
            print("Sell: " + str(sell_price))
            print("Profit: " + str((sell_price*stocks)-(buy_price*stocks)))
            stocks = 0 
            print("Cash: " + str(cash))
            print(" --------- ") 
        return result
    
    def backtest_rsi(self, cash):

        self.scan_rsi_over_70()
        self.scan_rsi_under_50()
        stocks = 0
        i = 0
        while i < len(self.df):
        #for i in range(0, len(self.df)):            
            try:
                if self.df['rsi_over_70'][i] == 1:
                    
                    #Kjøp
                    buy_price = self.df['close'][i]
                    #a = self.atr[i]
                    #stop_loss = buy_price - a*3

                    stocks = math.floor(cash / buy_price)
                    cash = cash%buy_price
                    print(self.df.index[i])
                    print("Buy: " + str(buy_price))
                    
                    a = i
                    while self.df['rsi_under_50'][a] == 0:
                       a = a+1  
                       if a== len(self.df):
                           break
                    i=a
                    #while self.df['close'][i] > stop_loss or self.df['slowk_drops_under_80'][i] == 0:
                     #   i = i+1  
                    #Selg Aksjer
                    sell_price = self.df['close'][i]
                    cash = cash + (sell_price*stocks)
                    
                    print(self.df.index[i])
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
                pass
        #Selg aksjer hvis det er noe igjen
        if stocks > 0:
            sell_price = self.df['close'][i-1]
            cash = cash + (sell_price*stocks)
                    
            print(self.df.index[i-1])
            print("Sell: " + str(sell_price))
            print("Profit: " + str((sell_price*stocks)-(buy_price*stocks)))
            stocks = 0 
            print("Cash: " + str(cash))
            print(" --------- ") 
        return cash

    def scan_obv(self):

        try:
           
            l = len(self.df)
            wma1 = self.df.iloc[l]['wma']
            wma2 = self.df.iloc[l]['wma']
            obv1 = self.df.iloc[l-1]['obv']
            obv2 = self.df.iloc[l-1]['obv']

            if wma1 < obv1 and wma2 > obv2:
                print("Found")
                return True
            else:
                print("No Symbol Found")
                return False
        except:
            print("Error")
            return False

    def scan_doublecross(self):
        try:
            
            self.stoch_crossover()
            self.macd_crossover()
            self.doublecross()
            #s.slowk_drops_under_80()
            l = len(self.df)
            h = self.df.iloc[l-1]['doublecross']
            h1 = self.df.iloc[l-2]['doublecross']
            #h2 = self.df.iloc[l-3]['doublecross']
            #h2 = self.df.iloc[l-3]['doublecross']
            #h3 = self.df.iloc[l-4]['doublecross']
            if h == 1 or h1 ==1: #or h2 == 1 or h3 == 1:
                print("Found")
                return True
            else:
                print("No Symbol Found")
                return False
        except:
            print("Error")
            return False

    def scan_rsi(self):
        try:
            
            self.scan_rsi_over_70()

            l = len(self.df)
            h = self.df.iloc[l-1]['rsi_over_70']
            h1 = self.df.iloc[l-2]['rsi_over_70']
            h2 = self.df.iloc[l-3]['rsi_over_70']
            h2 = self.df.iloc[l-3]['rsi_over_70']
            h3 = self.df.iloc[l-4]['rsi_over_70']
            if h == 1 or h1 ==1 or h2 == 1 or h3 == 1:
                print("Found")
                return True
            else:
                print("No Symbol Found")
                return False
        except:
            print("Error")
            return False

    def scan_rsi_over_70(self):
        self.df["rsi_over_70"] = 0
        rsi = abstract.RSI(self.df)
        for i in range(0, len(rsi)):            
            try:
                a = rsi[i]
                b = rsi[i+1]
                #k krysser over 70
                if a < 70 and b > 70:
                    self.df['rsi_over_70'][i+1] = 1
            except:
                pass
        return self.df

    def scan_rsi_under_50(self):
        self.df["rsi_under_50"] = 0
        rsi = abstract.RSI(self.df)
        for i in range(0, len(rsi)):            
            try:
                a = rsi[i]
                b = rsi[i+1]
                #k krysser under 50
                if a > 50 and b < 50:
                    self.df['rsi_under_50'][i+1] = 1
            except:
                pass
        return self.df

    def scan_macd(self):
        try:
            
            #self.stoch_crossover()
            self.macd_crossover()
            #self.doublecross()
            #s.slowk_drops_under_80()
            l = len(self.df)
            h = self.df.iloc[l-1]['doublecross']
            h1 = self.df.iloc[l-2]['doublecross']
            #h2 = self.df.iloc[l-3]['doublecross']
            #h2 = self.df.iloc[l-3]['doublecross']
            #h3 = self.df.iloc[l-4]['doublecross']
            if h == 1 or h1 ==1: #or h2 == 1 or h3 == 1:
                print("Found")
                return True
            else:
                print("No Symbol Found")
                return False
        except:
            print("Error")
            return False

    #Scan for bullish candlestick patterns:     Bullish Engulfing (2)Piercing Pattern (2)Bullish Harami (2) Hammer (1)Inverted Hammer (1)Morning Star (3)Bullish Abandoned Baby (3) 

    def scan2(self):
        try:
            cdl=[]# = None
            cdl.append(abstract.CDLENGULFING(self.df))        
            cdl.append(abstract.CDLPIERCING(self.df))       
            cdl.append(abstract.CDLHARAMI(self.df))       
            cdl.append(abstract.CDLHAMMER(self.df))        
            cdl.append(abstract.CDLINVERTEDHAMMER(self.df))        
            cdl.append(abstract.CDLMORNINGDOJISTAR(self.df))        
            cdl.append(abstract.CDLMORNINGSTAR(self.df))       
            cdl.append(abstract.CDLABANDONEDBABY(self.df)) 
            cdl.append(abstract.CDLKICKING(self.df))        
                   
             
            for i in range(0,9):
                for a in range(0,2):
                    if cdl[i][a] == 100:
                        print("Found")
                        print(i)
                        print(self.df.index[i])
        except:
            print("Error")
            return False

    def scan3(self):
        try:
            cdl=[]# = None
            cdl.append(abstract.CDLENGULFING(self.df))        
            cdl.append(abstract.CDLPIERCING(self.df))       
            cdl.append(abstract.CDLHARAMI(self.df))       
            cdl.append(abstract.CDLHAMMER(self.df))        
            cdl.append(abstract.CDLINVERTEDHAMMER(self.df))        
            cdl.append(abstract.CDLMORNINGDOJISTAR(self.df))        
            cdl.append(abstract.CDLMORNINGSTAR(self.df))       
            cdl.append(abstract.CDLABANDONEDBABY(self.df)) 
            cdl.append(abstract.CDLKICKING(self.df))        
                   
             
            for i in range(0,9):
                for a in range(0,2):
                    if cdl[i][a] == 100:
                        print("Found")
                        print(i)
                        print(self.df.index[i])
        except:
            print("Error")
            return False