"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
"""

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager

app = Flask(__name__)

app.config.from_object('config.base')

deploy_type = os.environ.get('VOWEL_DEPLOY', 'development')

if deploy_type in ['dev', 'development']:
    app.config.from_object('config.development')

elif deploy_type in ['prod', 'production']:
    app.config.from_object('config.production')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['PORT'] = int(os.environ.get('PORT', 8000))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['DEBUG'] = bool(os.environ.get('DEBUG', False))


if app.config['SQLALCHEMY_DATABASE_URI']:
    db = SQLAlchemy(app)

config = app.config

mail = Mail(app)

toolbar = DebugToolbarExtension(app)
_pyflakes = toolbar

login_manager = LoginManager(app)
