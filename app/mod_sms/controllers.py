import re

from app import app, tc, db
from app.mod_sms.models import UserGroup, User, Message
from app.mod_sms.views import (base_message, welcome_1, welcome_2,
                               confirm_welcome_2, opt_out)
from flask import request, make_response
from flask_restful import Resource, reqparse
from twilio import TwilioRestException

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


class BaseMessage(Resource):
    # TODO: For later similar operations of messages

    def __init__(self):
        # FIXME: This will have to change to a phone number pulled from the db
        self.twilio_phone_number = app.config.get('TWILIO_PHONE_NUMBER')
        self.request = MessageRequest()

    def save_message(self, request):
        if not isinstance(request, MessageRequest):
            raise TypeError("store_message requires type MessageRequest")

        user = User.read_user(phone=request.from_number)
        if not user:
            User.create_user(phone=request.from_number, active=True)
            user = User(phone=request.from_number)

        user_group = UserGroup.read_user_group(user_group_name='Canyon Time', active=True)

        message = Message.create_message(
            sms_message_sid=request.sms_message_sid,
            body=request.body,
            sms_status=request.sms_status,
            to_number=request.to_number,
            to_zip=request.to_zip,
            to_country=request.to_country,
            from_number=request.from_number,
            from_zip=request.from_zip,
            from_country=request.from_country
        )

        user.messages.append(message)
        User.update_user(user)

        # user_group.users.append(user)
        user_group.messages.append(message)
        UserGroup.update_user_group(user_group)

        # Will commit all updates from all classes
        db.session.commit()

        return user_group, user, message


class InboundMessage(BaseMessage):
    """docstring for InboundMessage"""

    def trigger_group_message(self, user_group, user, message):
        if not isinstance(user, User):
            raise('InboundMessage.trigger_group_message user requires type User')
        if not isinstance(user_group, UserGroup):
            raise('InboundMessage.trigger_group_message user_group requires type UserGroup')
        if not isinstance(message, Message):
            raise('InboundMessage.trigger_group_message message requires type Message')
        users_to_send = UserGroup.read_users(id=user_group.id)
        users_to_send.discard(user)

        resp = OutboundMessage.twiml_send_message(user_group=user_group, users=users_to_send,
                                                  sent_from_user=user, message=message,
                                                  template=base_message)

    def post(self):
        """accept incoming message"""
        user_group, user, message = self.save_message(self.request)
        # TODO: add regex matching for other path than trigger_group_message
        self.trigger_group_message(user_group=user_group, user=user, message=message)


class OutboundMessage(BaseMessage):
    """docstring for OutboundMessage"""

    @staticmethod
    def twiml_send_message(user_group, users, sent_from_user, message, template):
        while users:
            user = users.pop()
            formatted_message = template(
                **dict(
                    user=user,
                    fname=sent_from_user.fname,
                    lname=sent_from_user.lname,
                    body=message.body,
                )
            )
            try:
                _ = tc.messages.create(
                    to=user.phone,
                    from_=user_group.phone_number,
                    body=formatted_message,
                    # media_url=
                )
            except TwilioRestException as e:
                print(e)
            except Exception as other_exception:
                print(other_exception)

    def post(self):
        """Send message from API"""
        try:
            message = tc.messages.create(
                to=self.request.to_number,
                from_=self.twilio_phone_number,
                body=self.request.body
            )
        except TwilioRestException as e:
            print(e)
            return 400


class Group(BaseMessage):
    def get(self):
        """Reply to message with group information"""
        pass
