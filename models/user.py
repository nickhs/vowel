from flask.ext.security import UserMixin, RoleMixin

from app import db
from base import ModelMixin

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(UserMixin, ModelMixin, db.Model):
    __tablename__ = 'user'

    # FIXME unique?
    public_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(80))  # FIXME set to IP type?
    current_login_at = db.Column(db.String(80))  # FIXME set to IP type?
    login_count = db.Column(db.Integer())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, active=False, roles=[]):
        self.email = email
        self.password = password
        self.active = active
        self.roles += roles


class Role(RoleMixin, ModelMixin, db.Model):
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
