import inspect

from app import db

from base import ModelMixin


class Share(ModelMixin, db.Model):
    __tablename__ = 'share'

    originator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    read_date = db.Column(db.DateTime)

    def __init__(self, origin, receiver, article):
        super(Share, self).__init__()
        self.__add_relation(origin, 'originator_id')
        self.__add_relation(receiver, 'receiver_id')
        self.__add_relation(article, 'article_id')

    def __add_relation(self, item, attr):
        if not hasattr(self, attr):
            raise Exception("Passed in invalid attribute: %s" % attr)

        if inspect.isclass(type(item)):
            # Assume it's the right class
            # FIXME check the class meta?
            setattr(self, attr, item.id)
        elif type(item) is str:
            setattr(self, attr, item)
        else:
            raise Exception("Unknown type received: %s" % type(item))
