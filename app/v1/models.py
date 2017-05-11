from app import databases
from passlib.apps import custom_app_context as pwd_context


class Items(databases.Model):
    __tablename__ = 'BucketListItems'

    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(250))
    datecreated = databases.Column(databases.DateTime)
    date_modified = databases.Column(databases.DateTime)
    user = databases.Column(databases.Integer(), databases.ForeignKey('UserInfo.id'))

    def __init__(self, name):
        self.name = name

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def __repr__(self):
        return '<Items {}'.format(self.name)


class Users(databases.Model):
    __tablename__ = 'UserInfo'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    username = databases.Column(databases.String(250))
    password_hash = databases.Column(databases.String(300))

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
