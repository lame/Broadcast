from flask import request, Response
from flask_restful import Resource, reqparse
from twilio import TwilioRestException

from app import app, tc, db
from app.mod_sms.adapters import MessageRequest
from app.mod_sms.models import UserGroup, User, Message
from app.mod_sms.templates import base_message


class Test(Resource):
    """Just a test to show API is running"""

    def get(self):
        return True


class BaseMessage(Resource, MessageRequest):
    """docstring for BaseMessage"""

    def __init__(self):
        # FIXME: This will have to change to a phone number pulled from the db
        self.twilio_phone_number = app.config.get('TWILIO_PHONE_NUMBER')

    def save_message(self):
        # Phone number format validation
        message = Message(
            sms_message_sid=self.sms_message_sid,
            body=self.body,
            sms_status=self.sms_status,
            to_number=self.to_number,
            to_zip=self.to_zip,
            to_country=self.to_country,
            from_number=self.from_number,
            from_zip=self.from_zip,
            from_country=self.from_country
        ).create()

        user = User(phone=self.request.from_number).show()
        user.append_message(message)

        user_group = UserGroup(user_group_name='Canyon Time', active=True).show()
        user_group.append_message(message)

        message.commit()

        return user_group, request_user, message


class InboundMessage(BaseMessage):
    """docstring for InboundMessage"""

    def post(self):
        user_group, user, message = self.save_message(self.request)
        template = base_message(message=message, user=user, user_group=user_group)
        # TODO: add regex matching for other path than trigger_group_message
        OutboundMessage.trigger_group_message(user_group=user_group, user=user, message=message)


class OutboundMessage(BaseMessage):
    """docstring for OutboundMessage"""

    def trigger_group_message(self, user_group, user, message, template):
        users_to_send = user_group.show_users()
        users_to_send.discard(user)

        while users:
            self.post(user_group=user_group, users=users.pop(), sent_from_user=user, body=template)

        return Response(mimetype='text/xml')

    @staticmethod
    def post(user_group, users, sent_from_user, body):
        try:
            tc.messages.create(
                to=user.phone,
                from_=user_group.phone_number,
                body=template,
                # media_url=
            )
        except TwilioRestException as e:
            print(e)
        except Exception as other_exception:
            print(other_exception)
