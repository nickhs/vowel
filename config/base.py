DEBUG = True
SECRET_KEY = 'not_a_secret'
PORT = 8000
SQLALCHEMY_DATABASE_URI = 'sqlite://'

# Flask-Security
SECURITY_REGISTERABLE = True

# Flask-Mail
MAIL_SERVER = 'smtp.mandrillapp.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'fixme@fixme.com'
MAIL_PASSWORD = 'fixme'

# Flask Debug Toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Article Parsing
ARTICLE_PARSE_ENDPOINT = "http://api.diffbot.com/v2/article"
