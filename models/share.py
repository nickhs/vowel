from app import db

from base import ModelMixin


class Share(ModelMixin, db.Model):
    __tablename__ = 'share'
