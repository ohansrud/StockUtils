"""
Routes and views for the flask application.
"""
import numpy as np
from talib import abstract
import ystockquote as y
import pandas as pd
from pprint import pprint
from datetime import date, timedelta, datetime
import math
import sys 
import ystockquote as y
from flask import render_template, Response, jsonify, request
from FlaskWebProject1 import app
import json
import sys
from FlaskWebProject1.models.StockQuote import StockQuote as st

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""


    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
@app.route('/about/<ticker>')
def about(ticker):

    today = datetime.today()
    day = timedelta(days=1)
    year = timedelta(days=(365*2))
    start = today-year
    end = today-day
    try:
        s = st(ticker, str(start.strftime('%Y-%m-%d')), str(end.strftime('%Y-%m-%d')))    

        cash = 10000
        stocks = 0
    
        #cash = s.backtest_rsi(cash)
        #cash = s.backtest_doublecross(cash)
        msg = "Cash: " + str(cash) + ". Profit: " + str(cash-10000)
        #profit.append(item + ": " + str(cash-10000))
        #print("---------------------------------------")
        """Renders the about page."""
        return render_template(
            'chart.html',
            title=ticker,
            year=datetime.now().year,
            message=msg
        )
    except:
        return render_template(
            'stockDrawingTrendLines.html',
            title='Error',
            year=datetime.now().year,
            message=sys.exc_info()[0]
        )

#@app.route('/json/')
#@app.route('/json/<ticker>')
#def json(ticker):
#    today = datetime.today()
#    day = timedelta(days=1)
#    year = timedelta(days=(365*2))
#    start = today-year
#    end = today-day
#    try:
#        s = st(ticker, str(start.strftime('%Y-%m-%d')), str(end.strftime('%Y-%m-%d')))    



#        resp = jsonify(s.df['close'])
#        resp.status_code = 200

#        return resp
#    except:
#        resp = jsonify(data=sys.exc_info()[0])
#        resp.status_code = 500

#        return resp

@app.route('/json/')
@app.route('/json/<ticker>')
def json(ticker):
    today = datetime.today()
    day = timedelta(days=1)
    year = timedelta(days=(365*2))
    start = today-year
    end = today-day
    try:
        s = st(ticker, str(start.strftime('%Y-%m-%d')), str(end.strftime('%Y-%m-%d')))    
        s.df['index'] = s.df.index
        #subset = data_set[['open', 'high', 'low', 'close']]
        subset = s.df[['index', 'open', 'high', 'low', 'close']]

        tuples = [tuple(x) for x in subset.values]

        resp = jsonify(result=tuples)
        resp.status_code = 200

        return resp
    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(data)
        resp.status_code = 500

        return resp
    