from flask import jsonify, request
from FlaskWebProject1 import app
import json as j
from FlaskWebProject1.models.Scanners import *
from FlaskWebProject1.models.Backtester import *
from FlaskWebProject1.models.Portfolio import Portfolio
import jsonpickle

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
            outfile.seek(0)
            outfile.truncate()
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

    try:
        s = st(ticker, 1, 730)
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
    from FlaskWebProject1.models.Scanners import ScannerDoublecross, ScannerRSI
    try:
        if(scanner == "RSI70"):
            d = ScannerRSI()
            result = d.found
        elif(scanner == "Doublecross"):
            d = ScannerDoublecross()
            result = d.found
        #elif(scanner == "OBV"):
            #result = scanner_obv()
        #elif(scanner == "stoploss"):
            #result = scanner_stoploss()
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

@app.route('/api/portfolio/', methods=['GET'])
def get_portfolio():
    try:
        with open('FlaskWebProject1/data/portfolio.json') as data_file:
            data = j.load(data_file)
            p = jsonpickle.decode(data)
            jsonstring = jsonpickle.encode(p, unpicklable=False)
    except:
        p = Portfolio("Test", 10000);
        with open('FlaskWebProject1/data/portfolio.json', 'w') as data_file:
            jsonstring = jsonpickle.encode(p)
            j.dump(jsonstring, data_file)
        jsonstring = jsonpickle.encode(p, unpicklable=False)

    resp = jsonify(portfolio=jsonstring)
    resp.status_code = 200

    return resp


    data=sys.exc_info()[0]
    resp = jsonify(error=data)
    resp.status_code = 500

    return resp

@app.route('/api/portfolio', methods=['POST'])
def create_portfolio(method, ticker):
    try:
        p = Portfolio("Test", 10000);
        resp = jsonify(result=p.serialize)
        resp.status_code = 200

        return resp

    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500

        return resp


@app.route('/api/portfolio/buy/<ticker>', methods=['POST'])
def buy_position(ticker):
    amount = request.json['amount']
    try:
        with open('FlaskWebProject1/data/portfolio.json') as data_file:
            data = j.load(data_file)
            p = jsonpickle.decode(data)
    except:
        p = Portfolio("Test", 10000)
        data=sys.exc_info()[0]

    try:
        p.buy(ticker, amount)
        with open('FlaskWebProject1/data/portfolio.json', 'w') as data_file:
            jsonstring = jsonpickle.encode(p)
            j.dump(jsonstring, data_file)

        resp = jsonify(result="OK")
        resp.status_code = 200

        return resp

    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500

        return resp


@app.route('/api/portfolio/sell/<ticker>', methods=['POST'])
def sell_position(ticker):
    try:
        with open('FlaskWebProject1/data/portfolio.json') as data_file:
            data = j.load(data_file)
            p = jsonpickle.decode(data)
    except:
        p = Portfolio("Test", 10000)
        data=sys.exc_info()[0]

    try:
        p.sell(ticker)
        with open('FlaskWebProject1/data/portfolio.json', 'w') as data_file:
            jsonstring = jsonpickle.encode(p)
            j.dump(jsonstring, data_file)

        resp = jsonify(result="OK")
        resp.status_code = 200

        return resp

    except ValueError:
        data=sys.exc_info()[0]
    except:
        data=sys.exc_info()[0]
        resp = jsonify(error=data)
        resp.status_code = 500

        return resp

