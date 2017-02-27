from app import db
from app.mod_sms.custom_errors import DuplicateUserGroupException, \
    DuplicateUserException, DuplicateMessageException

ADMIN_ROLE = 1
USER_ROLE = 0


groups_to_users = db.Table(
    'groups_to_users',
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')))


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
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    # FIXME: Need to add user group admins later
    # group_admin = db.Column(db.Integer, db.ForeignKey('user.id'))

    messages = db.relationship('Message', backref='user_group', lazy='dynamic')
    groups_to_users = db.relationship('User', secondary=groups_to_users,
                                      backref=db.backref('users_in_group', lazy='dynamic'))

    def __init__(self, phone, name=None, active=True):
        self.active = active
        self.name = name
        self.phone = phone

    def show(self):
        return self.query.filter_by(active=self.active, phone=self.phone).first()

    def update(self):
        db.session.add(self)
        return self

    def destroy(self):
        db.session.delete(self)
        return self

    # FIXME: Need to call Twilio for new number here:
    def create(self):
        if not self.show():
            self.groups_to_users.append(self.user)
            db.session.add(self)
        else:
            raise DuplicateUserGroupException('Duplicate User Group: {0}'.format(self.id))

    def show_users(self):
        return {user for user in self.query.filter_by(id=self.id).first().groups_to_users if user.active}

    def append_message(self, message, user):
        if user.active and self in user.users_groups:
            self.messages.append(message)
        db.session.add(self)


class User(Base):
    """
    1:Many User -> UserGroup
    1:Many User -> Messages
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(35))
    lname = db.Column(db.String(35))
    phone = db.Column(db.String(15), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    # FIXME: Need to add user groups owned/admined
    # admin = db.relationship('UserGroup', backref='user', lazy='dynamic')

    onboarding = db.relationship('UserOnboarding', uselist=False, backref="user_onboard")
    messages = db.relationship('Message', backref='user_messages', lazy='dynamic')
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
        db.session.add(self)
        return self

    def show(self):
        user = self.query.filter_by(phone=self.phone, active=self.active)
        if user.first():
            return user.first()

        self.active = False
        return self.create()
        # FIXME: Need to send the new user into new user flow

    def edit(self):
        db.session.add(self)
        return self

    def update(self):
        db.session.add(self)
        return self

    def destroy(self, phone, active=True):
        db.session.delete(self)
        return self

    def append_message(self, message):
        self.messages.append(message)
        db.session.add(self)

    @property
    def is_active(self):
        return self.active


class UserOnboarding(Base):
    """
    One to One -> User
    """
    __tablename__ = 'user_onboarding'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    step = db.Column(db.Integer, nullable=False, default=0)
    opt_in = db.Column(db.Boolean, nullable=False, default=False)
    fname = db.Column(db.String, nullable=True)
    lname = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)

    user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, step=0, completed=False, opt_in=False,
                 fname=None, lname=None, phone=None):
        self.step = step
        self.completed = False
        self.opt_in = opt_in
        self.fname = fname
        self.lname = lname
        self.phone = phone


class Message(Base):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sms_message_sid = db.Column(db.String(160), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sms_status = db.Column(db.String(20), nullable=False)
    to_number = db.Column(db.String(15), nullable=False)
    to_zip = db.Column(db.Integer, nullable=False)
    to_city = db.Column(db.String, nullable=True)
    to_country = db.Column(db.String(5), nullable=False)
    from_number = db.Column(db.String(15), nullable=False)
    from_zip = db.Column(db.Integer, nullable=False)
    from_city = db.Column(db.String, nullable=True)
    from_country = db.Column(db.String(5), nullable=False)
    media_url = db.Column(db.String, nullable=True)
    media_content_type = db.Column(db.String, nullable=True)
    api_version = db.Column(db.String, nullable=True)
    num_segments = db.Column(db.Integer, nullable=True)

    user_group_id = db.Column(db.Integer, db.ForeignKey('user_groups.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, body, sms_message_sid, sms_status, to_number, media_url,
                 to_country, from_number, from_country, media_content_type,
                 to_city=None, to_zip=None, from_city=None, from_zip=None):
        self.body = body
        self.sms_message_sid = sms_message_sid
        self.sms_status = sms_status
        self.to_number = to_number
        self.to_zip = self._fill_null_zip(to_zip)
        self.to_city = to_city
        self.to_country = to_country
        self.from_number = from_number
        self.from_zip = self._fill_null_zip(from_zip)
        self.from_city = from_city
        self.from_country = from_country
        self.media_url = media_url
        self.media_content_type = media_content_type

    def create(self):
        if not self.show():
            db.session.add(self)
        else:
            raise DuplicateMessageException('Duplicate Message SID: {0}'.format(self.sms_message_sid))
        return self

    def show(self):
        message = self.query.filter_by(sms_message_sid=self.sms_message_sid)
        return message.first()

    def edit(self):
        db.session.add(self)
        return self

    def update(self):
        db.session.add(self)
        return self

    def destroy(self):
        db.session.delete(self)
        return self

    @staticmethod
    def _fill_null_zip(zip):
        if not zip:
            return 0
        return zip
