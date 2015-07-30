from datetime import date, timedelta, datetime
import ystockquote as y
from flask import render_template, Response, jsonify, request
from FlaskWebProject1 import app
import json as j
import sys
from FlaskWebProject1.models.StockQuote import StockQuote as st
from FlaskWebProject1.models.Scanners import *
from FlaskWebProject1.models.BacktestingResult import BacktestingResult, BacktestingTrade
from FlaskWebProject1.models.Backtester import *

@app.route('/api/getannotations/<ticker>', methods=['GET'])
def getannotations(ticker):
    try:
        with open('FlaskWebProject1/data/'+ticker+'.json') as data_file:
            data = j.load(data_file)
        resp = jsonify({'Status': "Ok", 'Annotations': data})
        resp.status_code = 200
        return resp
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500
        return resp\


@app.route('/api/saveannotations/<ticker>', methods=['POST'])
def saveannotations(ticker):
    try:
        a = request.json['annotations']
        with open('FlaskWebProject1/data/'+ticker+'.json', 'w') as outfile:
            j.dump(a, outfile)
        resp = jsonify(Status="Ok")
        resp.status_code = 200
        return resp
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500
        return resp


@app.route('/api/getchartdata/<ticker>')
def getchartdata(ticker):
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

@app.route('/api/scan/<scanner>')
def scan(scanner):
    try:
        if(scanner == "RSI70"):
            result = scanner_rsi()
        elif(scanner == "Doublecross"):
            result = scanner_doublecross()
        elif(scanner == "OBV"):
            result = scanner_obv()
        elif(scanner == "stoploss"):
            result = scanner_stoploss()
        resp = jsonify(result=result)
        resp.status_code = 200

        return resp
    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500

        return resp

@app.route('/api/backtest/<method>/<ticker>')
def backtest(method, ticker):
    try:
        if(method == "doublecross"):
            b = Backtester_DoubleCross(ticker)
            result = b.result
        elif (method == "rsi"):
            b = Backtester_RSI(ticker)
            result = b.result
        resp = jsonify(result=result.serialize)
        resp.status_code = 200

        return resp

    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500

        return resp