from talib import abstract
import ystockquote as y
import pandas as pd
import sys
from pprint import pprint
from datetime import datetime, timedelta
import time
from FlaskWebProject1.models.Annotation import Annotation

class StockQuote(object):

    def __init__(self, ticker, start_day= None, length=730):
        self.ticker = ticker
        if(start_day == None):
            today = datetime.today()
            start_day = today - timedelta(days=length)
            start_str = str(start_day.strftime('%Y-%m-%d'))
            end_str = str(today.strftime('%Y-%m-%d'))
        else:
            start_str = start_day
            #start = time.strptime(start_day, "%Y-%m-%d")
            start = datetime.strptime(start_str, "%Y-%m-%d")
            end_day = start + timedelta(days=length)
            end_str = str(end_day.strftime('%Y-%m-%d'))

        i = y.get_historical_prices(ticker, start_str, end_str)

        #Lag Pandas DataFrame
        self.df = pd.DataFrame(i)

        #Snu Dataframe
        self.df = self.df.transpose()

        #endre datatype til float
        self.df = self.df.astype(float)
        self.df = self.df.rename(columns={'Close': 'close', 'High': 'high', 'Open': 'open', 'Low': 'low','Volume': 'volume'})

        stoch = abstract.STOCH(self.df, 14, 1, 3)
        macd = abstract.MACD(self.df)
        atr = abstract.ATR(self.df)
        obv = abstract.OBV(self.df)
        rsi = abstract.RSI(self.df)

        self.df['atr'] = pd.DataFrame(atr)
        self.df['obv'] = pd.DataFrame(obv)
        self.df['rsi'] = pd.DataFrame(rsi)

        #kombinerer to dataframes
        self.df = pd.merge(self.df, pd.DataFrame(macd), left_index=True, right_index=True, how='outer')
        self.df = pd.merge(self.df, stoch, left_index=True, right_index=True, how='outer')

    #Scanner etter tilfeller grafen krysser med inntegnede linjer (Annotations)
    def inter(self):
        self.df["inter"] = 0
        self.df["ann_cross"] = 0
        crossings = []
        annotations = Annotation.query.filter_by(linkedTo = self.ticker).all()
        for ann in annotations:
            ann_id = ann.id
            dx = ann.xValueEnd - ann.xValue
            dy = ann.yValueEnd -ann.yValue
            #Increase per day
            delta = float(dy/dx)
            #28.7 = 1438041600000
            #t = 1438041600000
            #Difference in days
            #y = time.localtime(min(ann.xValueEnd, ann.xValue)/1000)
            #start_str = time.strftime('%Y-%m-%d', y)
            #y = time.localtime(max(ann.xValueEnd, ann.xValue)/1000)
            #end_str = time.strftime('%Y-%m-%d', y)

            #st = self.df.index.get_indexer_for((self.df[self.df.index == start_str].index))
            #end = self.df.index.get_indexer_for((self.df[self.df.index == end_str].index))

            #if(st>0):
            #    i = st
            #else:
            #    i=0

            #if(end>0):
            #    end = end
            #else:
            #

            end=len(self.df)
            i=end-30

            while i < end:
            #for s in self.df:
                try:
                    date_time = self.df.index[i]
                    #type = type(date_time)
                    try:
                        date_time = date_time._data[0]
                    except:
                        pass
                    pattern = '%Y-%m-%d'

                    #Current date of i in epoch format
                    d = int(time.mktime(time.strptime(date_time, pattern))*1000)
                    #Distance from start of line to current date
                    dt = (d-ann.xValue)

                    #If i is not before the start of the line
                    if(dt>0):

                        t = ann.yValue + (dt*delta)
                        self.df['inter'][i] =t
                        last_t = float(self.df.iloc[i-1]['inter'])
                        #If last_has a value. Otherwise it cannot be compared
                        if(last_t>0):
                            #Close value of prev day
                            last_close = float(self.df.iloc[i-1]['close'])
                            #Close value of prev day
                            close = float(self.df.iloc[i]['close'])
                            if int(last_t) > int(last_close) and int(t) < int(close):
                                r = "Grafen krysser opp over linja"
                                self.df["ann_cross"][i] = 1
                                index = self.df.index[i]
                                crossings.append({'date':index, 'value':t, 'direction': 'up'})
                            elif int(last_t) < int(last_close) and int(t) > int(close):
                                r = "Grafen krysser ned under linja"
                                self.df["ann_cross"][i] = 1
                                index = self.df.index[i]
                                crossings.append({'date':index, 'value':t, 'direction': 'down'})

                except:
                    d= sys.exc_info()
                i=i+1
            #days =  (dt/1000/3600/24)
        return self.df


    #Scanner etter tilfeller der Slow K krysser med Slow D
    def stoch_crossover(self):
        self.df["array_K_cross_down"] = 0
        self.df["array_D_cross_down"] = 0
        i=0
        try:
            for i in range(0, len(self.df)):            
                try:
                    #raise RuntimeError
                    index = self.df.index[i]
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
                #index = self.df.index[i]
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
                        print()
                        self.df['signal_cross_down'][i] = 1
            except:
                pass

        return self.df

    #Moving average 200
    def ma_200(self):
        ma_200 = abstract.MA(self.df, 200)
        self.df["ma_200"] = 0
        for i in range(199, len(self.df)):
            try:
                ma = ma_200[i]
                close = self.df.iloc[i]['close']

                #If Close pirce is higher tha MA200
                if ma < close:
                    self.df['ma_200'][i] = 1
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
                ma = self.df.iloc[i]['ma_200']
                k = self.df.iloc[i-1]['slowk']
                #k krysser under d
                if d == 1:
                    if s == 1 or s2 == 1 or s3 == 1 or s4 == 1 or s5 == 1:
                        #if k < 80:
                        #if ma ==1:
                        self.df['doublecross'][i] = 1
            except:
                pass

        return self.df

    def atr_stoploss(self):
        self.df["atr_stoploss"] = 0
        self.df["atr_takeprofit"] = 0

        for i in range(0, len(self.df)):
            try:
                prev_close = self.df.iloc[i-1]['close']
                atr = self.atr[i-1]
                high = self.df.iloc[i-4]['high']
                low = self.df.iloc[i-4]['low']
                stoploss = prev_close - (atr * 5)
                takeprofit = prev_close + (atr * 5)

                #High higher than atr * 5
                if high > takeprofit:
                    self.df['atr_takeprofit'][i] = 1
                elif low < stoploss:
                    self.df['atr_stoploss'][i] = 1
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