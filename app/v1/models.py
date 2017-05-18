from datetime import datetime
from app import databases
from passlib.apps import custom_app_context as pwd_context


class Items(databases.Model):
    __tablename__ = 'BucketListItems'

    id = databases.Column(databases.Integer,
                          primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(250))
    datecreated = databases.Column(databases.DateTime,
                                   default=datetime.utcnow())
    date_modified = databases.Column(databases.DateTime,
                                     default=datetime.utcnow(),
                                     onupdate=datetime.utcnow())
    bucketlist_id = databases.Column(databases.Integer(),
                                     databases.ForeignKey('Bucketlist.id'))

    def __init__(self, name, id):
        self.name = name
        self.bucketlist_id = id

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def __repr__(self):
        return '<Items {}'.format(self.name)


class BucketList(databases.Model):
    __tablename__ = 'Bucketlist'
    id = databases.Column(databases.Integer,
                          primary_key=True, autoincrement=True)
    user = databases.Column(databases.Integer(),
                            databases.ForeignKey('UserInfo.id'))
    name = databases.Column(databases.String(255))
    items = databases.relationship('Items', backref="Bucketlist")
    date_created = databases.Column(databases.DateTime,
                                    default=datetime.utcnow())
    date_modified = databases.Column(
        databases.DateTime, default=datetime.utcnow(),
        onupdate=datetime.utcnow())
    created_by = databases.Column(databases.Integer)

    def __init__(self, name):
        self.name = name

    def save(self):
        databases.session.add(self)
        databases.session.commit()


class Users(databases.Model):
    __tablename__ = 'UserInfo'
    id = databases.Column(databases.Integer,
                          primary_key=True, autoincrement=True)
    Bucket = databases.relationship('BucketList', backref='UserInfo')
    username = databases.Column(databases.String(250))
    password_hash = databases.Column(databases.String(300))

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
