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
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    users = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(Base):
    __tablename__ = 'user'

    user_fk = db.relationship('UserGroup', backref='user', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    phone = db.Column(db.Integer, unique=True)
    messages = db.Column(db.Text, db.ForeignKey('message.id'))

    def __init__(self, phone, fname=None, lname=None):
        self.phone = phone
        self.fname = fname
        self.lname = lname


class Message(Base):
    message_fk = db.relationship('User', backref='message', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    sms_message_sid = db.Column(db.Text)
    status = db.Column(db.Text)
