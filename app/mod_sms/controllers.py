import re

from app import app, tc, db
from app.mod_sms.models import UserGroup, User, Message
from flask import request
from flask_restful import Resource, reqparse
from twilio import twiml, TwilioRestException

FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')



class Test(Resource):
    """Just a test to show API is running"""

    def get(self):
        return True


class MessageRequest():

    def __init__(self):
        kwargs = self.parse_request()
        self.sms_status = kwargs.get('sms_status')
        self.sms_message_sid = kwargs.get('sms_message_sid')
        self.body = kwargs.get('body')

        self.to_number = kwargs.get('to')
        self.to_city = kwargs.get('to_city')
        self.to_state = kwargs.get('to_state')
        self.to_zip = kwargs.get('to_zip')
        self.to_country = kwargs.get('to_country')

        self.from_number = kwargs.get('from')
        self.from_city = kwargs.get('from_city')
        self.from_state = kwargs.get('from_state')
        self.from_zip = kwargs.get('from_zip')
        self.from_country = kwargs.get('from_country')

    # TODO: Move this to a mixin
    @staticmethod
    def convert(name):
        s1 = FIRST_CAP_RE.sub(r'\1_\2', name)
        return ALL_CAP_RE.sub(r'\1_\2', s1).lower()

    # TODO: Move this to a mixin
    @classmethod
    def parse_request(cls):
        message_reqparse = reqparse.RequestParser()

        if request.values:
            message_reqparse.add_argument('SmsStatus', type=str, required=True, location='values')
            message_reqparse.add_argument('SmsMessageSid', type=str, required=True, location='values')
            message_reqparse.add_argument('Body', type=str, required=True, location='values')

            message_reqparse.add_argument('To', type=str, required=True, location='values')
            message_reqparse.add_argument('ToCity', type=str, required=True, location='values')
            message_reqparse.add_argument('ToState', type=str, required=True, location='values')
            message_reqparse.add_argument('ToCountry', type=str, required=True, location='values')
            message_reqparse.add_argument('ToZip', type=str, required=True, location='values')

            message_reqparse.add_argument('From', type=str, required=True, location='values')
            message_reqparse.add_argument('FromCity', type=str, required=True, location='values')
            message_reqparse.add_argument('FromState', type=str, required=True, location='values')
            message_reqparse.add_argument('FromCountry', type=str, required=True, location='values')
            message_reqparse.add_argument('FromZip', type=str, required=True, location='values')

        else:
            message_reqparse.add_argument('To', type=str, required=True, help='to_phone_number not provided', location='json')
            message_reqparse.add_argument('Body', type=str, required=False, location='json')

        return {cls.convert(x): y for x, y in message_reqparse.parse_args().items()}


    def store_message(self, request):
        if not isinstance(request, MessageRequest):
            raise TypeError("store_message requires type MessageRequest")

        import ipdb; ipdb.set_trace()
        user = User.query.filter_by(phone=request.from_number).first()

        user_group = UserGroup.query.filter_by(user_group_name='meet me in the canyons', active=True).first()
        user_group.users.append(user)

        message = Message(
            body=request.body,
            sms_message_sid=request.sms_message_sid,
            sms_status=request.sms_status,
            to_number=request.to_number,
            to_zip=request.to_zip,
            to_country=request.to_country,
            from_number=request.from_number,
            from_zip=request.from_zip,
            from_country=request.from_country
        )

        user.messages.append(message)
        user_group.messages.append(message)

        db.session.add(user)
        db.session.add(user_group)
        db.session.add(message)
        db.session.commit()


class BaseMessage(Resource):
    # TODO: For later similar operations of messages
    pass


class ReceiveMessage(BaseMessage):
    """docstring for ReceiveMessage"""

    def post(self):
        """accept incoming message"""
        self.request = MessageRequest()
        self.store_message(self.request)
        resp = twiml.Response()
        resp.message('hello world')
        return str(resp)


class SendMessage(BaseMessage):
    """docstring for SendMessage"""

    def __init__(self):
        # FIXME: This will have to change to a phone number pulled from the db
        self.twilio_phone_number = app.config.get('TWILIO_PHONE_NUMBER')

    def post(self):
        """Send message from API"""
        self.request = MessageRequest()
        try:
            message = tc.messages.create(
                to=self.request.to_number,
                from_=self.twilio_phone_number,
                body=self.request.body
            )
            return 200

        except TwilioRestException as e:
            print(e)
            return 400


class Group(BaseMessage):
    def get(self):
        """Reply to message with group information"""
        pass
