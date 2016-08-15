from app import api
from app.mod_sms.controllers import(
    Test,
    ReceiveMessage,
    SendMessage,
    Group,
)

api.add_resource(Test, '/')
api.add_resource(SendMessage, '/send')
api.add_resource(ReceiveMessage, '/receive')
api.add_resource(Group, '/group')
