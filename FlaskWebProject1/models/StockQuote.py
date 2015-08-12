from talib import abstract
import ystockquote as y
import pandas as pd
import sys
from pprint import pprint
from datetime import datetime, timedelta

class StockQuote(object):
    """description of class"""
    sma = []
    stoch = []
    macd = []
    atr = []
    obv = []
    rsi = []
    df = []

    def __init__(self, ticker, start_days, end_days):

        today = datetime.today()
        day = timedelta(days=start_days)
        year = timedelta(days=end_days)
        start = today-year
        end = today-day
        start_str = str(start.strftime('%Y-%m-%d'))
        end_str = str(end.strftime('%Y-%m-%d'))

        i = y.get_historical_prices(ticker, start_str, end_str)

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
        self.ma_200 = abstract.MA(df2, 200)



        #kombinerer to dataframes
        self.df = pd.merge(df2, pd.DataFrame(self.macd), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, self.stoch, left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.atr), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.obv), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.rsi), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, pd.DataFrame(self.ma_200), left_index=True, right_index=True, how='outer')
    
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
                        l2 = self.df['array_K_cross_down'][i]
                    else:
                        #d krysser under k
                        if k < d and k2 > d2:
                            self.df['array_D_cross_down'][i] = 1
                            g2 = self.df['array_D_cross_down'][i]
                except:
                    pass
                    #pprint(sys.exc_info())
                    
        except:
            pass
            #print(sys.exc_info())
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

    # Scanner etter tilfeller der prisen er høyere enn ma_200
    def price_higher_than_ma_200(self):
        self.df["price_higher_than_ma_200"] = 0

        for i in range(0, len(self.df)):
            try:
                ma = self.df.iloc[i]['ma_200']
                close = self.df.iloc[i]['close']

                #k krysser under d
                if close > ma:
                    self.df['price_higher_than_ma_200'][i] = 1
            except:
                pass

        return self.df
    '''
    Scanner etter tilfeller der macd_crossover skjer 1-4 dager etter
    stochastic crossover
    '''
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

    def wma_obv(self):

        df2 = self.df
        df2.rename(columns={'obv': 'close'})
        try:
            self.wma_obv = abstract.WMA(df2, 233)
        except:
            pprint(sys.exc_info())

    def slowk_drops_under_80(self):
        self.df["slowk_drops_under_80"] = 0
        self.df["test"] = 0
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


    def scan_wma_obv(self):
        self.scan_wma_obv_sloping_up()
        try:
           
            l = len(self.df)
            wma1 = self.df.iloc[l-2]['both_sloping_up']
            wma2 = self.df.iloc[l-1]['both_sloping_up']

            if wma1 == 0 and wma2 == 1:
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
            #self.price_higher_than_ma_200()
            #s.slowk_drops_under_80()
            l = len(self.df)
            h = self.df.iloc[l-1]['doublecross']
            h1 = self.df.iloc[l-2]['doublecross']
            #ma = self.df.iloc[l-1]['price_higher_than_ma_200']
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

    def scan_wma_obv_sloping_up(self):
        self.df["both_sloping_up"] = 0

        wma = abstract.WMA(self.df, 233)

        df2 = self.df
        df2.rename(columns={'obv': 'close'})
        wma_obv = abstract.WMA(df2, 233)

        for i in range(0, len(wma_obv)):
            try:
                a = wma_obv[i-1]
                b = wma_obv[i]
                c = wma[i-1]
                d = wma[i]

                if a < b and c <  d:
                    self.df['both_sloping_up'][i] = 1
            except:
                pass

        return self.df

    def scan_macd(self):
        try:
            self.macd_crossover()
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

    def scan_stoploss(self):
        try:
            self.slowk_drops_under_80()
            l = len(self.df)
            prev_close = self.df.iloc[l-2]['close']
            low = self.df.iloc[l-1]['low']
            atr3 = self.atr[l-1] * 5
            stoploss = prev_close -atr3
            slowk_under_80 = self.df['slowk_drops_under_80'][l-1]

            if low < stoploss or slowk_under_80 == 1:
                print("Found")
                return True
            else:
                print("No Symbol Found")
                return False
        except:
            print("Error")
            return False

    #Scan for bullish candlestick patterns:     Bullish Engulfing (2)Piercing Pattern (2)Bullish Harami (2) Hammer (1)Inverted Hammer (1)Morning Star (3)Bullish Abandoned Baby (3) 

    def scan_cdlbullish(self):
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

    def scan_cdl_bearish(self):
        try:
            cdl=[]
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