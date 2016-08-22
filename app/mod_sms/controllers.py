from app import app, tc, db
from app.mod_sms.models import UserGroup, User, Message
from flask import request
from flask_restful import Resource, reqparse
from twilio import twiml, TwilioRestException


class Test(Resource):
    """Just a test to show API is running"""

    def get(self):
        return True


class BaseMessage(Resource):
    def __init__(self):
        message_reqparse = reqparse.RequestParser()

        if not request.values:
            message_reqparse.add_argument('to_phone_number', type=str, required=True, help='to_phone_number not provided', location='json')
            message_reqparse.add_argument('body', type=str, required=False, location='json')

        else:
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

        self.kwargs = message_reqparse.parse_args()
        super(BaseMessage, self).__init__()

    def store_message(self, **kwargs):
        message = Message(
            body=kwargs.get('Body'),
            message_sid=kwargs.get('SmsMessageSid'),
            status=kwargs.get('SmsStatus'),
            to_number=kwargs.get('To'),
            to_zip=kwargs.get('ToZip'),
            to_country=kwargs.get('ToCountry'),
            from_number=kwargs.get('From'),
            from_zip=kwargs.get('FromZip'),
            from_country=kwargs.get('FromCountry')
        )

        user = User.query.filter_by(phone=kwargs.get('From')).first()
        user.messages.append(message)

        user_group = UserGroup.query.filter_by(user_group_name='meet me in the canyons').first()
        user_group.messages.append(message)
        user_group.users.append(user)

        db.session.add(user)
        db.session.add(user_group)
        db.session.add(message)
        db.session.commit()


class ReceiveMessage(BaseMessage):
    """docstring for ReceiveMessage"""

    def post(self):
        """accept incoming message"""
        self.store_message(**self.kwargs)
        resp = twiml.Response()
        resp.message('hello world')
        return str(resp)


class SendMessage(BaseMessage):
    """docstring for SendMessage"""

    def post(self):
        """Send message from API"""
        try:
            message = tc.messages.create(
                to=self.kwargs.get('to_phone_number'),
                from_=app.config.get('TWILIO_PHONE_NUMBER'),
                body=self.kwargs.get('body')
            )
            return 200

        except TwilioRestException as e:
            print(e)
            return 400


class Group(BaseMessage):
    def get(self):
        """Reply to message with group information"""
        pass
