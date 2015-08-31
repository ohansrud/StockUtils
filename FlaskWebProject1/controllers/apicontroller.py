from flask import jsonify, request
from FlaskWebProject1 import app
#import json as j
from FlaskWebProject1.models.Scanners import ScannerDoublecross, ScannerRSI, ScannerStoploss

from FlaskWebProject1.models.Scanners import *
from FlaskWebProject1.models.Backtester import *
from FlaskWebProject1.models.Portfolio import Portfolio ,Position
from FlaskWebProject1.models.Annotation import Annotation
from FlaskWebProject1.models.Scrapers import Scraper
from FlaskWebProject1 import db
import jsonpickle
from datetime import datetime

@app.route('/api/tickers/', methods=['GET'])
def gettickers():
    try:
        s = Scraper()
        tickers = s.OL()
        resp = jsonify({'Success': True, 'result': tickers, 'msg': str(len(tickers))+' tickers found'})
        resp.status_code = 200
        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500
        return resp


@app.route('/api/getannotations/<ticker>', methods=['GET'])
def getannotations(ticker):
    try:
        data = Annotation.query.filter_by(linkedTo = ticker).all()
        for ann in data:
            ann = ann.extend()
        annotations = jsonpickle.encode(data)
        if(len(data)>0):
            msg = str(len(data))+' annotations found'
        else:
            msg = 'No annotations found'
        resp = jsonify({'Success': True, 'Annotations': annotations, 'msg': msg})
        resp.status_code = 200
        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500
        return resp


@app.route('/api/saveannotations/<ticker>', methods=['POST'])
def saveannotations(ticker):
    try:
        annotations = request.json['annotations']
        for a in annotations:
            try:
                #Get annotation from db
                ann = Annotation.query.get(a['id'])

                ann = ann.extend()
            except:
                #Save annotation in db
                if(a['xValue']>a['xValueEnd']):
                    x = a['xValueEnd']
                    xEnd = a['xValue']
                    y = a['yValueEnd']
                    yEnd = a['yValue']
                else:
                    xEnd = a['xValueEnd']
                    x = a['xValue']
                    yEnd = a['yValueEnd']
                    y = a['yValue']

                ann = Annotation(a['linkedTo'], x, y, xEnd, yEnd, "path")
                ann = ann.extend()
                db.session.add(ann)
        #save changes
        db.session.commit()
        annotations = Annotation.query.filter_by(linkedTo = ticker).all()
        resp = jsonify({'Success':True, 'msg':str(len(annotations)) + ' Annotations saved', 'result': jsonpickle.encode(annotations)})
        resp.status_code = 200
        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500
        return resp


@app.route('/api/getchartdata/<ticker>')
def getchartdata(ticker):
    try:
        s = st(ticker, None, 730)

        s.df['index'] = s.df.index
        subset = s.df[['index', 'open', 'high', 'low', 'close', 'volume']]

        #s.df['index'] = s.df.index
        try:
            crossings = s.inter()
        except:
            pass
        tuples = [tuple(x) for x in subset.values]

        resp = jsonify({'Success':True, 'result':tuples, 'msg': 'Chart found'})
        resp.status_code = 200

        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

        return resp


@app.route('/api/scan/<scanner>')
def scan(scanner):
    try:
        if(scanner == "RSI70"):
            d = ScannerRSI()
            result = d.found
        elif(scanner == "Doublecross"):
            d = ScannerDoublecross()
            result = d.found
        elif(scanner == "intersections"):
            d = ScannerCrossings()
            result = d.found
        elif(scanner == "stoploss"):
            d = ScannerStoploss()
            result = d.found
        resp = jsonify({'Success':True, 'result':result})
        resp.status_code = 200

        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
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
        res=jsonpickle.encode(result, unpicklable=False)
        resp = jsonify({'Success':True, 'result':res})
        resp.status_code = 200

        return resp

    except ValueError:
        data=sys.exc_info()[0]
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

        return resp


@app.route('/api/portfolio/<id>', methods=['GET'])
def get_portfolio(id):
    try:
        portfolio = Portfolio.query.get(id)

        portfolio.getportfoliovalue()
        jsonstring = jsonpickle.encode(portfolio)
        resp = jsonify({'Success':True, 'result':jsonstring})
        resp.status_code = 200
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

    return resp


@app.route('/api/portfolio/', methods=['GET'])
def get_portfolios():
    try:
        portfolios = Portfolio.query.all()
        for p in portfolios:
            p.getportfoliovalue()
        jsonstring = jsonpickle.encode(portfolios)
        resp = jsonify({'Success':True, 'result':jsonstring})
        resp.status_code = 200

        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

    return resp


@app.route('/api/portfolio', methods=['POST'])
def create_portfolio(method, ticker):
    try:
        name = request.json['name']
        cash = request.json['cash']
        p = Portfolio(name, int(cash));
        jsonstring = jsonpickle.encode(p)
        resp = jsonify({'Success':True, 'result':jsonstring})
        resp.status_code = 200

        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

        return resp


@app.route('/api/portfolio/<id>/buy/<ticker>', methods=['POST'])
def buy_position(id, ticker):
    amount = request.json['amount']
    try:
        portfolio = Portfolio.query.get(id)
        portfolio.buy(ticker, amount)
        resp = jsonify({'Success':True})
        resp.status_code = 200

        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

        return resp


@app.route('/api/portfolio/<id>/sell/<pos>', methods=['POST'])
def sell_position(id, pos):
    try:
        portfolio = Portfolio.query.get(id)
        position = Portfolio.open_positions.query.get(pos)
        portfolio.sell(position)

        resp = jsonify({'Success':True})
        resp.status_code = 200

        return resp
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str(exc_type)[18:-2] + ": " + str(exc_obj)[1:-1]
        resp = jsonify({'Success':False, 'error':error})
        resp.status_code = 500

        return resp