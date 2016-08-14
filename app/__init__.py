from configparser import SafeConfigParser
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from twilio.rest import TwilioRestClient


app = Flask(__name__)
env = 'PRODUCTION'

app.config.from_object('config.Development')
parser = SafeConfigParser()

# FIXME: This needs to read off dev machine by user acct
parser.read('instances/kuhlryan.cfg')

# FIXME: Needs to pull config based on env var
app.config.update(
    TWILIO_PHONE_NUMBER=parser.get(env, 'TWILIO_PHONE_NUMBER'),
    TWILIO_ACCOUNT_SID=parser.get(env, 'TWILIO_ACCOUNT_SID'),
    TWILIO_ACCOUNT_AUTH=parser.get(env, 'TWILIO_ACCOUNT_AUTH'),
)

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
tc = TwilioRestClient(
    app.config.get('TWILIO_ACCOUNT_SID'),
    app.config.get('TWILIO_ACCOUNT_AUTH')
)

from app.mod_sms import views, models, controllers
