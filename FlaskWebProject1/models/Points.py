from zigzag import peak_valley_pivots
from pandas import Series, to_datetime
import sys

class Points(object):
    def __init__(self, dataframe):
        try:

            dataframe.df['index'] = to_datetime(dataframe.df.index)
            sub = Series(dataframe.df.high, index=dataframe.df.index)

            pivots = peak_valley_pivots(sub, 0.1, -0.1)
            self.points = {}
            i = 0
            while i < len(dataframe.df):
                if (pivots[i] != 0):
                    self.points[dataframe.df.index[i]] = pivots[i]
                i = i + 1
        except ValueError:
            data=sys.exc_info()[0]
        except:
            data=sys.exc_info()[0]

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'points'         : self.points
       }