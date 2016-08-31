import os


class Base(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    CSRF_ENABLED = True
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Base):
    DEBUG = True
    SECRET_KEY = 'Replace_With_SecretKey'
    DATABASE_QUERY_TIMEOUT = 0.5
    ACCOUNT_SID = 'Replace with Account SID'
    AUTH_TOKEN = 'Replace with Auth Token'
    PHONE_NUMBER = 'Replace with Twillio Phone Number'


class Production(Base):
    DEBUG = False
    SECRET_KEY = 'Replace_With_SecretKey'
    DATABASE_QUERY_TIMEOUT = 0.5
    ACCOUNT_SID = 'Replace with Account SID'
    AUTH_TOKEN = 'Replace with Auth Token'
    PHONE_NUMBER = 'Replace with Twillio Phone Number'
