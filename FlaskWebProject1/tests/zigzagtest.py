__author__ = 'ohansrud'

import pandas as pd
import pandas.io.data as web
from zigzag import peak_valley_pivots, max_drawdown, compute_segment_returns, pivots_to_modes
from FlaskWebProject1.models.StockQuote import StockQuote as st
from dateutil.parser import parse


X = web.get_data_yahoo('AAPL')['Adj Close']


dt = parse("2015-01-01")


s = st("AAPL", "2014-08-04", "2015-08-04")

#s.df.index =



s.df['index'] = pd.to_datetime(s.df.index)


#subset = s.df[['close']]

sub = pd.Series(s.df.close, index=s.df.index)

pivots = peak_valley_pivots(sub, 0.01, -0.01)
from flask import jsonify

#resp = jsonify(result=pivots)
points = {}

i = 0
while i < len(s.df):

    if (pivots[i] != 0):
        points[s.df.index[i]] = pivots[i]

    i=i+1

print points
resp = jsonify(result=points)

