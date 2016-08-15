from app import db


# TODO: Change to many-to-many relationship
# For now this will only have a one-to-many relationship
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class UserGroup(Base):
    """
    1:Many UserGroup -> User
    1:Many UserGroup -> Message
    """
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    user_group_name = db.Column(db.String(60), unique=True)

    users = db.relationship('User', backref='user_group', lazy='dynamic')
    messages = db.relationship('Message', backref='user_group', lazy='dynamic')

    def __init__(self, user_group_name, active=True):
        self.active = active
        self.user_group_name = 'meet me in the canyons'


class User(Base):
    """
    1:Many User -> UserGroup
    1:Many User -> Messages
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(35))
    lname = db.Column(db.String(35))
    phone = db.Column(db.String(15), unique=True, nullable=False)

    # Authorisation Data: role & status
    active = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)

    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, phone, active=True, role='U', fname=None, lname=None):
        self.role = role
        self.phone = phone
        self.fname = fname
        self.lname = lname
        self.active = active


class Message(Base):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    message_sid = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    to_number = db.Column(db.String(15), nullable=False)
    to_zip = db.Column(db.Integer, nullable=False)
    to_country = db.Column(db.String(2), nullable=False)
    from_number = db.Column(db.String(15), nullable=False)
    from_zip = db.Column(db.Integer, nullable=False)

    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, body, message_sid, status, to_number,
                 to_zip, to_country, from_number, from_zip, from_country):
        self.body = body
        self.message_sid = message_sid
        self.status = status
        self.to_number = to_number
        self.to_zip = to_zip
        self.to_country = to_country
        self.from_number = from_number
        self.from_zip = from_zip
        self.from_country = from_country
