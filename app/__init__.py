import os

from configparser import SafeConfigParser
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from twilio.rest import TwilioRestClient

app = Flask(__name__)

# ENV Vars
try:
  ENV = os.environ['ENV']
  ENV in ('STAGING', 'PRODUCTION')
except:
  raise EnvironmentError('Environmental variable "BROADCAST_ENV" not found or unrecognized value')

app.config.from_object('config.' + ENV)
parser = SafeConfigParser()
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
tc = TwilioRestClient(
    app.config.get('TWILIO_ACCOUNT_SID'),
    app.config.get('TWILIO_ACCOUNT_AUTH')
)

# FIXME
from app.mod_sms import views, models, controllers, routes
