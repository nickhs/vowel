from datetime import datetime
from urlparse import urlparse

from app import db

from base import ModelMixin


class Article(ModelMixin, db.Model):
    __tablename__ = 'article'

    url = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime)
    author = db.Column(db.String(255))

    parse_date = db.Column(db.DateTime)

    shares = db.relationship('Share', backref='article',
            lazy='dynamic')

    def __init__(self, url):
        super(Article, self).__init__()
        self.url = url

    def is_parsed(self):
        if self.parse_date is None:
            return False

        if self.parse_date > datetime.utcnow():
            return True

        return False

    def get_domain(self):
        return urlparse(self.url).netloc
