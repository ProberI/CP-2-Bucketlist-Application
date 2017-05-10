from app import databases


class Users(databases.Model):
    __tablename__ = 'UserInfo'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(250))
    email = databases.Column(databases.String(300))
    password = databases.Column(databases.String(300))


class Items(databases.Model):
    __tablename__ = 'BucketListItems'

    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(250))
    datecreated = databases.Column(databases.DateTime)
    date_modified = databases.Column(databases.DateTime)
    # user = databases.Column(databases.Integer, databases.ForeignKey('UserInfo.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Items {}'.format(self.name)
