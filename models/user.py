from app import db
from base import ModelMixin
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(ModelMixin, db.Model):
    __tablename__ = 'user'

    # FIXME unique?
    public_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(80))  # FIXME set to IP type?
    current_login_ip = db.Column(db.String(80))  # FIXME set to IP type?
    login_count = db.Column(db.Integer(), default=0)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    originating_shares = db.relationship('Share', backref='originator',
            lazy='dynamic', foreign_keys='Share.originator_id')

    receiving_shares = db.relationship('Share', backref='receiver',
            lazy='dynamic', foreign_keys='Share.receiver_id')

    def __init__(self, email, password=None, active=False, roles=[]):
        super(User, self).__init__()
        self.email = email

        if password:
            self.set_password(password, False)

        self.active = active
        self.roles += roles

    def get_name(self):
        return self.email

    def set_password(self, password, save=True):
        pwd_hash = pwd_context.encrypt(password)
        self.password = pwd_hash

        if save:
            self.save()

    def check_password(self, password, request=None):
        ok = pwd_context.verify(password, self.password)

        if not ok:
            return False

        if request:
            self.last_login_at = self.current_login_at
            self.current_login_at = datetime.utcnow()
            self.last_login_ip = self.current_login_ip
            self.current_login_ip = request.remote_addr
            self.login_count += 1
            self.save()

        return True

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter(cls.email == username).first()

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


class Role(ModelMixin, db.Model):
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
