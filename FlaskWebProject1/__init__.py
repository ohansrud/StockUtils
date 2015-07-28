"""
The flask application package.
"""
from flask import render_template, make_response
from flask import Flask
app = Flask(__name__)

import FlaskWebProject1.controllers.maincontroller
#import FlaskWebProject1.controllers.apicontroller