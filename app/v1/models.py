from app import databases
from passlib.hash import pbkdf2_sha256

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


class Items(databases.Model):
    __tablename__ = 'BucketListItems'

    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(250))
    datecreated = databases.Column(databases.DateTime, default=databases.func.current_timestamp())
    date_modified = databases.Column(databases.DateTime, default=databases.func.current_timestamp())
    bucketlist_id = databases.Column(databases.Integer(), databases.ForeignKey('Bucketlist.id'))

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
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    user = databases.Column(databases.Integer(), databases.ForeignKey('UserInfo.id'))
    name = databases.Column(databases.String(255))
    items = databases.relationship('Items', backref="Bucketlist")
    date_created = databases.Column(databases.DateTime, default=databases.func.current_timestamp())
    date_modified = databases.Column(databases.DateTime, default=databases.func.current_timestamp())
    created_by = databases.Column(databases.Integer)

    def __init__(self, name):
        self.name = name

    def save(self):
        databases.session.add(self)
        databases.session.commit()


class Users(databases.Model):
    __tablename__ = 'UserInfo'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    Bucket = databases.relationship('BucketList', backref='UserInfo')
    username = databases.Column(databases.String(250))
    password_hash = databases.Column(databases.String(300))

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def hash_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app_config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app_config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = Users.query.get(data['id'])
        return user
