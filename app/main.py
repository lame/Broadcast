from configparser import SafeConfigParser
from flask import Flask, g, request
from flask_restful import Resource, Api, reqparse
from twilio import twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)
api = Api(app)


class Test(Resource):
	"""Just a test to show API is running"""
	def get(self):
		return True


class BaseMessage(Resource):
	def __init__(self):
		parser = SafeConfigParser()
		parser.read('config/config.ini')

		self.twilio_phone_number = parser.get('TWILIO', 'PHONE_NUMBER')
		self.twilio_client = TwilioRestClient(
			parser.get('TWILIO', 'ACCOUNT_SID'), 
			parser.get('TWILIO', 'AUTH_TOKEN')
		)

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


class ReceiveMessage(BaseMessage):
	"""docstring for ReceiveMessage"""

	def post(self):
		"""accept incoming message"""
		resp = twiml.Response()
		resp.message('hello world')
		import ipdb; ipdb.set_trace()
		return str(resp)

class SendMessage(BaseMessage):
	"""docstring for SendMessage"""

	def post(self):
		"""Send message from API""" 
		try:
			message = self.twilio_client.messages.create(
				to=self.kwargs.get('to_phone_number'),
				from_=self.twilio_phone_number,
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

api.add_resource(Test, '/')
api.add_resource(SendMessage, '/send')
api.add_resource(ReceiveMessage, '/receive')
api.add_resource(Group, '/group')

if __name__ == "__main__":
	app.run(debug=True)
