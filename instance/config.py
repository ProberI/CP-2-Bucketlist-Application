import os


class MainConfig(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


class DevelopmentEnviron(MainConfig):
    DEBUG = True
    TESTING = True
    # URI to our development database
    SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost/bucketlist_db'


class TestingConfig(MainConfig):
    TESTING = True
    DEBUG = True
    # URI to our testing database
    SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost/test_db'


class ProductionConfig(MainConfig):
    DEBUG = False
    TESTING = False


# Dictionary with keys mapping to the different configuration environments
app_config = {
    'MainConfig': MainConfig,
    'DevelopmentEnviron': DevelopmentEnviron,
    'TestingConfig': TestingConfig,
    'ProductionConfig': ProductionConfig
}
