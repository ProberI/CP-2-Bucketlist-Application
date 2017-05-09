from app import databases
from databases import Column, Integer, String, DateTime, ForeignKey


class Items(databases.Model):
    __tablename__ = 'BucketListItems'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    datecreated = Column(DateTime)
    date_modified = Column(DateTime)
    user = Column(String(255), ForeignKey('Users.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Items {}'.format(self.name)


class Users(databases.Model):
    __tablename__ = 'UserInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    email = Column(String(300))
    password = Column(String(300))
