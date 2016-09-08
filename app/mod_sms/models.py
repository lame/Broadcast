from app import db
from app.mod_sms.custom_errors import DuplicateUserGroupException

ADMIN_ROLE = 1
USER_ROLE = 0


groups_to_users = db.Table('groups_to_users',
                           db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id')),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                           )


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    @staticmethod
    def commit():
        db.session.commit()
        return True


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
    group_admin = db.Column(db.Integer, nullable=False)

    groups_to_users = db.relationship('User', secondary=groups_to_users,
                                      backref=db.backref('users_in_group', lazy='dynamic'))
    messages = db.relationship('Message', backref='user_group', lazy='dynamic')

    def __init__(self, user_group_name, phone_number, group_admin, active=True):
        self.active = active
        self.user_group_name = user_group_name
        self.phone_number = phone_number
        self.group_admin = group_admin

    @classmethod
    def _find_user_group(cls, user_group_name, active=True):
        return cls.query.filter_by(user_group_name=user_group_name, active=active)

    @classmethod
    def read_user_group(cls, user_group_name, active):
        return cls._find_user_group(user_group_name=user_group_name, active=active).first()

    @classmethod
    def read_users(cls, id):
        return {user for user in UserGroup.query.filter_by(id=id).first().groups_to_users}

    @classmethod
    def create_user_group(cls, user_group_name, user, active=True):
        if not isinstance(user, User):
            raise TypeError('user is not of type User')

        # TODO: Need to call Twilio for new number here:
        phone_number = '+17868378095'

        if not cls.read_user_group(user_group_name=user_group_name, active=True):
                user_group = cls(
                    user_group_name=user_group_name,
                    active=True,
                    phone_number=phone_number,
                    group_admin=user.id,
                )
                user_group.groups_to_users.append(user)
                db.session.add(user_group)
                return user_group

        else:
            raise DuplicateUserGroupException

    @classmethod
    def update_user_group(cls, user_group):
        if not isinstance(user_group, UserGroup):
            raise TypeError('UserGroup.update_user_group requires type UserGroup')

        db.session.add(user_group)
        return user_group

    @classmethod
    def delete_user_group(cls, user_group_name, active=True):
        db.session.delete(cls.read_user_group(user_group_name=user_group_name, active=active))


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

    users_groups = db.relationship('UserGroup', secondary=groups_to_users,
                                   backref=db.backref('groups_of_user', lazy=True))
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, phone, active=True, role='U', fname=None, lname=None):
        self.role = role
        self.phone = phone
        self.fname = fname
        self.lname = lname
        self.active = active

    # FIXME: Move some of these into magic methods
    # FIXME: Lazy commit
    @classmethod
    def _find_user(cls, phone, active=True):
        return cls.query.filter_by(phone=phone, active=active)

    @classmethod
    def read_user(cls, phone, active=True):
        return cls._find_user(phone=phone, active=active).first()

    @classmethod
    def create_user(cls, phone, fname=None, lname=None, active=True, role=USER_ROLE):
        if not cls.read_user(phone):
            user = cls(
                phone=phone,
                fname=fname,
                lname=lname,
                active=active,
                role=role
            )
            db.session.add(user)
            return user

    @classmethod
    def update_user(cls, user):
        if not isinstance(user, cls):
            raise TypeError('User.update_user.user needs to be type User')

        db.session.add(user)
        return user

    @classmethod
    def delete_user(cls, phone, active=True):
        db.session.delete(cls.read_user(phone=phone, active=active))


class Message(Base):
    __tablename__ = 'message'

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

    @classmethod
    def _find_message(cls, sms_message_sid):
        return cls.query.filter_by(sms_message_sid=sms_message_sid)

    @classmethod
    def read_message(cls, sms_message_sid):
        return cls._find_message(sms_message_sid).first()

    @classmethod
    def create_message(cls, sms_message_sid, body, sms_status, to_number,
                       to_zip, to_country, from_number, from_zip, from_country):

        message = cls(
            sms_message_sid=sms_message_sid,
            body=body,
            sms_status=sms_status,
            to_number=to_number,
            to_zip=to_zip,
            to_country=to_country,
            from_number=from_number,
            from_zip=from_zip,
            from_country=from_country
        )
        db.session.add(message)
        return message

    @classmethod
    def delete_message(cls, sms_message_sid):
        db.session.delete(cls._find_message(sms_message_sid=sms_message_sid))
