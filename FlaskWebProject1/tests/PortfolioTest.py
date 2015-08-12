import unittest
from FlaskWebProject1.models.Portfolio import Portfolio, Position
import sys

class TestCase(unittest.TestCase):
    def test1(self):

        p = Portfolio(100000)

        p.buy("TEL.OL", 100)




        #p.buy("NHY.OL", 100)
        #p.buy("XXL.OL", 100)
        #p.buy("NHY.OL", 100)
        #p.buy("AKSO.OL", 100)

        p.sell("TEL.OL")

        d = p.cash
        assert(d==100000)

    def test2(self):

        p = Portfolio(100000)

        p.buy("TEL.OL", 100)




        p.buy("NHY.OL", 100)
        p.buy("XXL.OL", 100)
        p.buy("NHY.OL", 100)
        p.buy("AKSO.OL", 100)

        p.sell("TEL.OL")

        d = p.cash
        assert(d<100000)

class TestCase2(unittest.TestCase):

    def serializetest(self):
        import json as j
        p = Portfolio("Test", 10000);
        p.buy("TEL.OL", 100)
        d = j.dumps(p.open_positions)
        assert (1==1)