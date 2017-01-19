from flask import request, Response
from flask_restful import Resource
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

    @staticmethod
    def save_message(parsed_request):
        # Phone number format validation
        message = Message(
            sms_message_sid=parsed_request.sms_message_sid,
            body=parsed_request.body,
            sms_status=parsed_request.sms_status,
            to_number=parsed_request.to_number,
            to_zip=parsed_request.to_zip,
            to_country=parsed_request.to_country,
            from_number=parsed_request.from_number,
            from_zip=parsed_request.from_zip,
            from_country=parsed_request.from_country
        ).create()

        user = User(phone=parsed_request.from_number).show()
        user.append_message(message)

        # FIXME: this is a hack
        user_group = UserGroup(user_group_name='Canyon Time', active=True).show()
        user_group.append_message(message)

        message.commit()

        return user_group, request_user, message


class InboundMessage(BaseMessage):
    """docstring for InboundMessage"""

    def post(self):
        user_group, user, message = self.save_message(self.request())
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
