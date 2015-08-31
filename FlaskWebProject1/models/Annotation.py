from FlaskWebProject1 import db
from datetime import datetime, timedelta
from time import time
import sys

class Annotation(db.Model):
    __tablename__ = "annotation"
    id = db.Column(db.Integer, primary_key=True)
    linkedTo= db.Column(db.String(80))
    #xValue= db.Column(db.DateTime)
    xValue= db.Column(db.Float)
    yValue= db.Column(db.Float)
    #xValueEnd= db.Column(db.DateTime)
    xValueEnd= db.Column(db.Float)
    yValueEnd= db.Column(db.Float)
    shapetype= db.Column(db.String(80))

    def __init__(self, linkedTo, xValue, yValue, xValueEnd, yValueEnd, shapetype):
        self.linkedTo = linkedTo
        self.xValue = xValue
        self.yValue = yValue
        self.xValueEnd = xValueEnd
        self.yValueEnd = yValueEnd
        self.shapetype = shapetype

    def extend(self):

        #Get current date
        #today = datetime.today()
        try:
            today = float(time()*1000)

            dx = float(self.xValueEnd-self.xValue)
            dy = float(self.yValueEnd-self.yValue)
            #Increase per day
            delta = float(dy/dx)

            #Difference between Annotation and current date
            dt = (today-self.xValueEnd)

            t = self.yValueEnd + (dt*delta)
            self.yValueEnd = t
            self.xValueEnd = today
            print(t)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type)

        return self
    #def getintersectionpoint(self):





    def getintersectionpoints(self, t):

        dx = float(max(self.xValueEnd, self.xValue) - min(self.xValueEnd, self.xValue))
        dy = float(max(self.yValueEnd, self.yValue) - min(self.yValueEnd, self.yValue))

        #Increase per day
        delta = float(dy/dx)
        #28.7 = 1438041600000
        #t = 1438041600000
        #Difference in days
        dt = (t-min(self.xValueEnd, self.xValue))
        #days =  (dt/1000/3600/24)

        return min(self.yValueEnd, self.yValue) + (dt*delta)