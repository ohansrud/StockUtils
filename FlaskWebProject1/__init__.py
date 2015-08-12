"""
The flask application package.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3
import sys
import os

app = Flask(__name__)

import FlaskWebProject1.controllers.maincontroller
import FlaskWebProject1.controllers.apicontroller



