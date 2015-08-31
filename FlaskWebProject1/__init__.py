"""
The flask application package.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.socketio import SocketIO, emit, SocketIOServer

#import logging
#logging.basicConfig()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
db = SQLAlchemy(app)



from FlaskWebProject1.models.Portfolio import *
from FlaskWebProject1.models.Annotation import *
db.create_all()
#socketio = SocketIO(app)

#@socketio.on('connect')
#def test_connect():
#    emit('my response', {'data': 'Connected'})

#@socketio.on('my event')
#def test_message(message):
#    emit('my response', {'data': message['data']})
#    print("Test")

#@socketio.on('my broadcast event', namespace='/test')
#def test_message(message):
#    emit('my response', {'data': message['data']}, broadcast=True)



#@socketio.on('disconnect', namespace='/test')
#def test_disconnect():
#    print('Client disconnected')

#socketio.run(app)

import FlaskWebProject1.controllers.maincontroller
import FlaskWebProject1.controllers.apicontroller


from datetime import datetime

#a = Annotation("Test", 1411231314, 100.4, 1411231314, 120.1, "path")
#port = Portfolio("Test", 100000)
#position = Position("TEl.OL", datetime.today(), 100, 10)
#port.open_positions.append(position)

#db.session.add(a)
#db.session.commit()


#print(p)
#db.session.add(port)
#db.session.commit()

#portfolio = Portfolio.query.all()
#position = Portfolio.query.all()

#a = Annotation.query.all()
#data = Annotation.query.all()

#data = Annotation.query.all()
#for d in data:
#    db.session.delete(d)
#db.session.commit()
#print(a)

#data = Annotation.query.filter_by(linkedTo = 'Test').all()

