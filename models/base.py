from datetime import datetime

from app import db


class ModelMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        self.created_date = datetime.utcnow()
        self.modified_date = datetime.utcnow()

        columns = self.__table__.columns
        for key, value in kwargs.iteritems():
            if key in columns:
                setattr(self, key, value)
            else:
                raise Exception("Got key: %s without matching table attribute" % key)

    def _change_made(self):
        self.modified_date = datetime.utcnow()

    def remove(self):
        self._change_made()
        self.deleted = True
        self.save()

    def delete(self):
        self._change_made()
        db.session.delete(self)
        db.session.commit()

    def save(self):
        self._change_made()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.id)

    def to_dict(self, included=set(), excluded=set()):
        exclude = set(['modified_date', 'deleted'])
        exclude.update(excluded)
        exclude.difference_update(included)

        if 'deleted' in excluded and self.deleted:
            return

        ret = {}

        for column in self.__table__.columns:
            if column.name in exclude:
                continue

            ret[column.name] = getattr(self, column.name)

        return ret
