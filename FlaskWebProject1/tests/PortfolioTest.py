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