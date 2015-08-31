import unittest
from FlaskWebProject1.models.StockQuote import StockQuote as st
import sys
import time
import datetime

class TestCase(unittest.TestCase):

    def Test_StockQuoteConstructor1(self):
        start_str = "2015-01-01"
        start = datetime.datetime.strptime(start_str, "%Y-%m-%d")
        s = st("GSF.OL", "2015-01-01")

        print(s)

    def Test_StockQuoteConstructor2(self):
        s2 = st("GSF.OL", None, 20)

        print(s2)

    def Test_StockQuoteConstructor2(self):
        s2 = st("GSF.OL", "2015-01-01", 200)

        print(s2)

    def Test_MACDCrossover1(self):
        s = st("GSF.OL", "2014-05-15", 700)
        s.macd_crossover()

        assert(s.df.ix["2015-05-11"]["macd_cross_down"]==1)
        assert(s.df.ix["2015-05-26"]["macd_cross_down"]==1)
        assert(s.df.ix["2015-03-11"]["macd_cross_down"]==1)
        assert(s.df.ix["2015-05-19"]["signal_cross_down"]==1)
        assert(s.df.ix["2015-04-09"]["signal_cross_down"]==1)

        print(s)

    def Test_StochCrossover1(self):
        s = st("GSF.OL", "2014-05-15", 700)
        s.stoch_crossover()

        assert(s.df.ix["2015-05-11"]["array_K_cross_down"]==1)
        assert(s.df.ix["2015-05-26"]["array_K_cross_down"]==1)
        assert(s.df.ix["2015-03-11"]["array_K_cross_down"]==1)
        assert(s.df.ix["2015-05-19"]["array_D_cross_down"]==1)
        assert(s.df.ix["2015-04-09"]["array_D_cross_down"]==1)

        print(s)
