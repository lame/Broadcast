from flask import request, Response, session
from flask_restful import Resource
from twilio import TwilioRestException
from twilio.twiml import Response as TwiMLResponse

from app import tc
from app.mod_sms.adapters import MessageRequest
from app.mod_sms.models import UserGroup, User, Message
from app.mod_templates.base_message import base_message
from app.mod_templates.failure import failure_message


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
            to_city=parsed_request.to_city,
            to_country=parsed_request.to_country,
            from_number=parsed_request.from_number,
            from_zip=parsed_request.from_zip,
            from_city=parsed_request.from_city,
            from_country=parsed_request.from_country,
            media_url=parsed_request.media_url,
            media_content_type=parsed_request.media_content_type
        ).create()

        # from nose.tools import set_trace; set_trace()
        user = User(phone=parsed_request.from_number).show()
        user.append_message(message)

        user_group = UserGroup(phone=parsed_request.to_number, active=True).show()
        user_group.append_message(message, user)

        message.commit()

        return user_group, user, message

    # FIXME: Need to setup proper logging
    @staticmethod
    def send_message(user_group, to_user, body, media_url=None):
        if to_user.active:
            try:
                tc.messages.create(
                    to=to_user.phone,
                    from_=user_group.phone,
                    body=body,
                    media_url=media_url
                )
            except TwilioRestException as e:
                print(e)
            except Exception as other_exception:
                print(other_exception)

    @staticmethod
    def purchase_phone_number(user, area_code=None):
        try:
            purchased_number = tc.phone_numbers.purchase(area_code=user.phone[2:5])
        except:
            purchased_number = tc.phone_numbers.purchase(area_code=310)

        # FIXME: The sms_url should presumably be an ENV Var
        purchased_number.update(sms_method='POST', sms_url='https://broadcast-production.herokuapp.com/inbound')
        return purchased_number


class InboundMessage(BaseMessage):
    """docstring for InboundMessage"""

    def post(self):
        try:
            user_group, user, message = self.save_message(self.request())
            body = base_message(message=message, user=user, user_group=user_group)
            # TODO: add regex matching for other path than trigger_group_message
            OutboundMessage.trigger_group_message(user_group=user_group, user=user, message=message, body=body)
            # FIXME: Need to add this to logger
            # logger.info('Message {message_sid} sent at {datetime}'.format(message_sid=message.sms_message_sid, datetime=str(datetime.now())))
        except Exception as e:
            return Response('Server Error, Please try again later, {0}'.format(e), status=500, mimetype='text/plain; charset=utf-8')

        return Response(status=204, mimetype='text/plain; charset=utf-8')


class OutboundMessage(BaseMessage):
    """docstring for OutboundMessage"""

    @classmethod
    def trigger_group_message(cls, user_group, user, message, body):
        users = user_group.show_users()
        users.discard(user)

        while users:
            cls.send_message(user_group=user_group, to_user=users.pop(), body=body, media_url=message.media_url)

    @classmethod
    def trigger_message(cls, user_group, user, body):
        cls.send_message(user_group=user_group, user=user, body=body)


class FailedMessage(BaseMessage):
    """There was a message failure in InboundMessage and the API returned a 5XX"""

    def get(self):
        resp = TwiMLResponse()
        resp.sms = failure_message()
        return str(resp)
