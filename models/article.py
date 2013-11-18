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

    shares = db.relationship('Share', backref='article',
            lazy='dynamic')

    def __init__(self, url):
        super(Article, self).__init__()
        self.url = url
