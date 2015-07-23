"""
Routes and views for the flask application.
"""
#import numpy as np
#from talib import abstract
#import ystockquote as y
#import pandas as pd
#from pprint import pprint
from datetime import date, timedelta, datetime
#import math
import sys 
import ystockquote as y
from flask import render_template, Response, jsonify, request, send_from_directory
from FlaskWebProject1 import app
import json as j
import sys
from FlaskWebProject1.models.StockQuote import StockQuote as st
from FlaskWebProject1.models.Scanners import scanner_doublecross, scanner_rsi
import time


@app.route('/')
def root():
    #"""Renders the home page."""
#    return send_from_directory('FlaskWebProject1/templates', 'ng-layout.html')
    return render_template('ng-layout.html')


@app.route('/bla')
def bla():
    """Renders the home page."""
    return render_template('ng-layout.html')

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


#@app.route('/chart')
#@app.route('/chart/<ticker>')
#def chart(ticker):
#    return render_template(
#        'ng-layout.html',
#        ticker=ticker,
#        year=datetime.now().year,
#        message=''
#    )

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
            'ng-layout.html'
        )
    except:
        return render_template(
            'ng-layout.html',
            title='Error',
            year=datetime.now().year,
            message=sys.exc_info()[0]
        )

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
        subset = s.df[['index', 'open', 'high', 'low', 'close', 'volume']]

        s.df['index'] = s.df.index

        tuples = [tuple(x) for x in subset.values]

        resp = jsonify(result=tuples)
        resp.status_code = 200

        return resp
    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500

        return resp

@app.route('/demo')
def demo():
    return render_template('ng-layout.html')

@app.route('/scan')
def scan():
    return render_template(
        'scan.html',
        title='Scanning',
        year=datetime.now().year,
        message=''
    )


@app.route('/scanner/')
def scanner():
    found = scanner_rsi()
    """Renders the about page."""
    resp = jsonify(result=found)
    resp.status_code = 200
    return resp


