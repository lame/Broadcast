import unittest

from nose.tools import assert_true

from app import app, db


class TestUselessTests(unittest.TestCase):
    # def setup(self):
    #     app.config['TESTING'] = True
    #     app.config['WTF_CSRF_ENABLED'] = False
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

    #     db.create_all()

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()

    def test_nothing(self):
        assert_true(True)

    # def test_sms(self):
    #   self.test_app = app.test_client()
    #   params = dict(
    #     ToCountry='US',
    #     ToState='FL',
    #     SmsMessageSid='SM01d24ae1a8dede74326bca2ab0986601',
    #     NumMedia=0,
    #     ToCity='MIAMI',
    #     FromZip=None,
    #     SmsSid='SM01d24ae1a8dede74326bca2ab0986601',
    #     FromState='CA',
    #     SmsStatus='received',
    #     FromCity='',
    #     Body='testtest',
    #     FromCountry='US',
    #     To='+17868378095',
    #     ToZip=33130,
    #     NumSegments=1,
    #     MessageSid='SM01d24ae1a8dede74326bca2ab0986601',
    #     AccountSid='ACd54f610007bb0fbf352df81d4fdff7dd',
    #     From='+16269882527',
    #     ApiVersion='2010-04-01'
    #   )

    #   response = self.test_app.post('/inbound', data=params)
    #   self.assertEquals(response.status, "200 OK")
