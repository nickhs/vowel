from app import db

from base import ModelMixin


class Article(ModelMixin, db.Model):
    __tablename__ = 'article'
