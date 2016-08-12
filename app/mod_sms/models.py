from app import db


# TODO: Change to many-to-many relationship
# For now this will only have a one-to-many relationship
class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    user_fk = db.relationship('UserGroup', backref='user', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    phone = db.Column(db.Integer, unique=True)
    messages = db.Column(db.Text, db.ForeignKey('message.id'))


class Message(db.Model):
    message_fk = db.relationship('User', backref='message', lazy='dynamic')

    id = db.Column(db.Integer, primary_key=True)
    text_message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
