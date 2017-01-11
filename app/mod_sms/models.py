from app import db
from app.mod_sms.custom_errors import DuplicateUserGroupException, \
    DuplicateUserException, DuplicateMessageException

ADMIN_ROLE = 1
USER_ROLE = 0


groups_to_users = db.Table(
    'groups_to_users',
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    @staticmethod
    def commit():
        db.session.commit()


class UserGroup(Base):
    """
    Many:Many UserGroup -> User
    1:Many UserGroup -> Message
    """
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    user_group_name = db.Column(db.String(60), unique=True)
    phone_number = db.Column(db.String(15), nullable=False)
    # FIXME: Need to add user group admins later
    # group_admin = db.Column(db.Integer, db.ForeignKey('user.id'))

    messages = db.relationship('Message', backref='user_group', lazy='dynamic')
    groups_to_users = db.relationship('User', secondary=groups_to_users,
                                      backref=db.backref('users_in_group', lazy='dynamic'))

    def __init__(self, user_group_name, phone_number=None, active=True):
        self.active = active
        self.user_group_name = user_group_name
        self.phone_number = phone_number

    def show(self):
        ug = self.query.filter_by(user_group_name=self.user_group_name, active=self.active)
        return ug.first()

    def update(self):
        db.session.add(self)

    def destroy(self):
        db.session.delete(self)

    # FIXME: Need to call Twilio for new number here:
    # def create(self):
    #     if not self.show():
    #         self.groups_to_users.append(self.user)
    #         db.session.add(self)
    #     else:
    #         raise DuplicateUserGroupException

    def show_users(self):
        return {user for user in self.query.filter_by(id=self.id).first().groups_to_users if user.active}


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
    active = db.Column(db.Boolean, nullable=False)
    # FIXME: Need to add user groups owned/admined
    # admin = db.relationship('UserGroup', backref='user', lazy='dynamic')

    messages = db.relationship('Message', backref='user', lazy='dynamic')
    users_groups = db.relationship('UserGroup', secondary=groups_to_users,
                                   backref=db.backref('groups_of_user', lazy=True))

    def __init__(self, phone, active=True, role='U', fname=None, lname=None):
        self.role = role
        self.phone = phone
        self.fname = fname
        self.lname = lname
        self.active = active

    # FIXME: Move some of these into magic methods
    # FIXME: Lazy commit
    def create(self):
        if not self.show():
            db.session.add(self)
        else:
            raise DuplicateUserException

    def show(self):
        user = self.query.filter_by(phone=self.phone, active=self.active)
        return user.first()

    def edit(self):
        db.session.add(self)

    def update(self):
        db.session.add(self)

    def destroy(self, phone, active=True):
        db.session.delete(self)


class Message(Base):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sms_message_sid = db.Column(db.String(160), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sms_status = db.Column(db.String(20), nullable=False)
    to_number = db.Column(db.String(15), nullable=False)
    to_zip = db.Column(db.Integer, nullable=False)
    to_country = db.Column(db.String(5), nullable=False)
    from_number = db.Column(db.String(15), nullable=False)
    from_zip = db.Column(db.Integer, nullable=False)
    from_country = db.Column(db.String(5), nullable=False)

    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, body, sms_message_sid, sms_status, to_number,
                 to_zip, to_country, from_number, from_zip, from_country):
        self.body = body
        self.sms_message_sid = sms_message_sid
        self.sms_status = sms_status
        self.to_number = to_number
        self.to_zip = to_zip
        self.to_country = to_country
        self.from_number = from_number
        self.from_zip = from_zip
        self.from_country = from_country

    def create(self):
        if not self.show():
            db.session.add(self)
        else:
            raise DuplicateMessageException

    def show(self):
        message = self.query.filter_by(sms_message_sid=sms_message_sid)
        return cls._find_message(sms_message_sid).first()

    def edit(self):
        db.session.add(self)

    def update(self):
        db.session.add(self)

    def destroy(self):
        db.session.delete(self)
