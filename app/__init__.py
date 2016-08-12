from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Development')
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.mod_sms import views, models, controllers
