from app import api
from app.mod_sms.controllers import (
    Test,
    InboundMessage,
    OutboundMessage
    # Group,
)

api.add_resource(Test, '/')
api.add_resource(OutboundMessage, '/outbound')
api.add_resource(InboundMessage, '/inbound')
# api.add_resource(Group, '/group')
