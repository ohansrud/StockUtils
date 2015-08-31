"""
This script runs the FlaskWebProject1 application using a development server.
"""
from os import environ
from FlaskWebProject1 import app
#from flask.ext.socketio import SocketIO, emit

#socketio = SocketIO(app)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
        #PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    PORT = 5000
    app.run(HOST, PORT, debug=True)
    #server = SocketIOServer(('127.0.0.1', 5000), app, resource='test', policy_server=False)
    #server.serve_forever()
    #socketio.run(app), HOST, 5000, resource="test")