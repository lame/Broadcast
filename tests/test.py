import os
import unittest

from app import app, db
from flask_fixtures import FixturesMixin

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FIXTURES_DIR = BASEDIR + '/tests/fixtures/'


class TwiMLTest(unittest.TestCase):
    fixtures = ['tests_fixture_data.json']
    app = app
    db = db

    def setUp(self):
        app.config['FIXTURES_DIRS'] = [FIXTURES_DIR]
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'test.db')
        db.create_all()

        self.test_app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assertTwiML(self, response):
        self.assertEquals(response.status, '200 OK')

    def message_kwargs(self, **kwargs):
        params = dict(
            ToCountry=kwargs.get('ToCountry'),
            ToState=kwargs.get('ToState'),
            SmsMessageSid=kwargs.get('SmsMessageSid'),
            NumMedia=kwargs.get('NumMedia'),
            ToCity=kwargs.get('ToCity'),
            FromZip=kwargs.get('FromZip'),
            SmsSid=kwargs.get('SmsSid'),
            FromState=kwargs.get('FromState'),
            SmsStatus=kwargs.get('SmsStatus'),
            FromCity=kwargs.get('FromCity'),
            Body=kwargs.get('Body'),
            FromCountry=kwargs.get('FromCountry'),
            To=kwargs.get('To'),
            ToZip=kwargs.get('ToZip'),
            NumSegments=kwargs.get('NumSegments'),
            MessageSid=kwargs.get('MessageSid'),
            AccountSid=kwargs.get('AccountSid'),
            From=kwargs.get('From'),
            ApiVersion=kwargs.get('ApiVersion')
        )

        formatted_params = '?'
        for key, value in params.items():
            formatted_params += '{key}={value}&'.format(key=key, value=value)
        return formatted_params

    def post_message(self, url, **kwargs):
        url = url + self.message_kwargs(**kwargs)
        return self.test_app.post(url)

    def get_message(self, url, **kwargs):
        return self.test_app.get(url, data=self.message_kwargs(**kwargs))


class TestMessages(FixturesMixin, TwiMLTest):
    def test_base_url_get_response(self):
        response = self.get_message(url='/')
        self.assertTwiML(response)

    # def test_sms(self):
    #     params = dict(
    #         ToCountry='US',
    #         ToState='FL',
    #         SmsMessageSid='SM01d24ae1a8dede74326bca2ab0986601',
    #         NumMedia=0,
    #         ToCity='MIAMI',
    #         FromZip=None,
    #         SmsSid='SM01d24ae1a8dede74326bca2ab0986601',
    #         FromState='CA',
    #         SmsStatus='received',
    #         FromCity='',
    #         Body='testtest',
    #         FromCountry='US',
    #         To='+19999999999',
    #         ToZip=33130,
    #         NumSegments=1,
    #         MessageSid='SM01d24ae1a8dede74326bca2ab0986601',
    #         AccountSid='ACd54f610007bb0fbf352df81d4fdff7dd',
    #         From='+18888888888',
    #         ApiVersion='2010-04-01'
    #     )

    #     response = self.post_message(url='/inbound', **params)
    #     self.assertTwiML(response)
