import re

from flask import request
from flask_restful import reqparse


FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')

class MessageRequest(object):

    def __init__(self):
        kwargs = self.parse_request()
        self.sms_status = kwargs.get('sms_status')
        self.sms_message_sid = kwargs.get('sms_message_sid')
        self.body = kwargs.get('body')

        self.to_number = self.validate_phone_numbers(kwargs.get('to'))
        self.to_city = kwargs.get('to_city')
        self.to_state = kwargs.get('to_state')
        self.to_zip = kwargs.get('to_zip')
        self.to_country = kwargs.get('to_country')

        self.from_number = self.validate_phone_numbers(kwargs.get('from'))
        self.from_city = kwargs.get('from_city')
        self.from_state = kwargs.get('from_state')
        self.from_zip = kwargs.get('from_zip')
        self.from_country = kwargs.get('from_country')

        self.num_segments = kwargs.get('num_segments')
        self.media_url = kwargs.get('media_url_0')
        self.api_version = kwargs.get('api_version')

    def request(self):
        return self

    # TODO: Move this to a mixin
    @staticmethod
    def convert(name):
        s1 = FIRST_CAP_RE.sub(r'\1_\2', name)
        return ALL_CAP_RE.sub(r'\1_\2', s1).lower()

    @staticmethod
    def validate_phone_numbers(phone_number):
        if phone_number[:1] != '+':
            phone_number = '+' + phone_number.strip()
        return phone_number

    def parse_request(self):
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

            message_reqparse.add_argument('MediaUrl0', type=str, required=False, location='values')
            message_reqparse.add_argument('NumSegments', type=int, required=False, location='values')
            message_reqparse.add_argument('ApiVersion', type=str, required=False, location='values')


        else:
            message_reqparse.add_argument('To', type=str, required=True, help='to_phone_number not provided', location='json')
            message_reqparse.add_argument('Body', type=str, required=False, location='json')

        return {self.convert(x): y for x, y in message_reqparse.parse_args().items()}
