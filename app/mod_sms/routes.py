from app import api
from app.mod_sms.controllers import (
    Test,
    InboundMessage,
    FailedMessage
)

api.add_resource(Test, '/')
api.add_resource(InboundMessage, '/inbound')
api.add_resource(FailedMessage, '/failed_message')
