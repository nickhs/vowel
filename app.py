"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
"""

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config.from_object('config.base')

app.config.from_object('config.production')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['PORT'] = int(os.environ.get('PORT', 8000))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['DEBUG'] = bool(os.environ.get('DEBUG', False))


if app.config['SQLALCHEMY_DATABASE_URI']:
    db = SQLAlchemy(app)

config = app.config

mail = Mail(app)

from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

toolbar = DebugToolbarExtension(app)
_pyflakes = toolbar
