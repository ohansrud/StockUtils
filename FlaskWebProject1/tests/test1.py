#!flask/bin/python
from mock import MagicMock, Mock
import unittest
from FlaskWebProject1.models.StockQuote import StockQuote as st
import numpy as np
import tradingmachine

class ProductionClass(object):
    data = "Test";
    def method(self):
        self.something(1, 2, 3)
    def something(self, a, b, c):
        pass

class A(object):
    data = "Test";
    def meth(self, a):
        return self.data;

class TestCase(unittest.TestCase):
    def test1(self):
        nickname = "Name"
        assert nickname == "Name"
        a = A()
        ma = Mock(wraps=a)
        ma.data = "D";

        f = ma.meth(1)

        #real = ProductionClass()
        #real.something = MagicMock()
        #real.method()

        s = st("TEL.OL", "2014-01-01", 200)
        test = "sdadsa"

class TradingmachineTest(unittest.TestCase):
    def test(self):

        tradingmachine.MarketSimulator

        





