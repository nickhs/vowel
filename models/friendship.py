from app import db

from base import ModelMixin


class Friendship(ModelMixin, db.Model):
    __tablename__ = 'friendship'

    originator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
