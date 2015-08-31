import unittest
import pandas as pd
import pandas.io.data as web
from zigzag import peak_valley_pivots, max_drawdown, compute_segment_returns, pivots_to_modes
from FlaskWebProject1.models.StockQuote import StockQuote as st
from dateutil.parser import parse

class TestCase(unittest.TestCase):
    def test_Valleys(self):
        s = st("AAPL", "2014-08-04", 200)
        s.df['index'] = pd.to_datetime(s.df.index)
        sub = pd.Series(s.df.close, index=s.df.index)

        pivots = peak_valley_pivots(sub, 0.01, -0.01)

        points = {}

        i = 0
        while i < len(s.df):

            if (pivots[i] != 0):
                #Dato = -1/1
                #points[s.df.index[i]] = pivots[i]
                #indexnummer = -1/1
                #points[i] = pivots[i]

                points[i] = s.df.iloc[i]['close']
            i=i+1

        print(points)

