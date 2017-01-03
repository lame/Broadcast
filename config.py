import os


class Base(object):
    # Flask Config
    basedir = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    DEBUG = False
    ENV = os.environ['BROADCAST_ENV']
    SECRET_KEY = os.environ.get('SECRET_KEY', '')

    # SQLAlchemy Config
    if not os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    DATABASE_QUERY_TIMEOUT = 0.5
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TWILIO Config
    try:
        TWILIO_ACCOUNT_SID=os.environ['TWILIO_ACCOUNT_SID_' + ENV]
        TWILIO_ACCOUNT_AUTH=os.environ['TWILIO_ACCOUNT_AUTH_' + ENV]
    except KeyError:
        raise('Missing Twilio environ variables')

class STAGING(Base):
    DEBUG = True
    SECRET_KEY = 'Replace_With_SecretKey'
    DATABASE_QUERY_TIMEOUT = 1.0

class PRODUCTION(Base):
    pass
