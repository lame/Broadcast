from app import db


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


class UserGroup(Base):
    """
    Many:Many UserGroup -> User
    1:Many UserGroup -> Message
    """
    __tablename__ = 'user_group'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    user_group_name = db.Column(db.String(60), unique=True)
    group_admin = db.Column(db.Integer, nullable=False)

    groups_to_users = db.relationship('User', secondary=groups_to_users,
                                      backref=db.backref('users_in_group', lazy='dynamic'))
    messages = db.relationship('Message', backref='user_group', lazy='dynamic')

    def __init__(self, user_group_name, active=True):
        self.active = active
        self.user_group_name = 'meet me in the canyons'


    @classmethod
    def _find_user_group(cls, id, active=True):
        return cls.query.filter_by(id=id, active=active)

    @classmethod
    def read_user_group(cls, id, active):
        return cls._find_user_group(id=id, active=active).first()

    @classmethod
    def create_user_group(cls, user_group_name, user=user, active=True):
        if not isinstance(user, User):
            raise TypeError('user is not of type User')

        if not _find_user_group(user_group_name=user_group_name):

                user_group = cls(
                    user_group_name=user_group_name,
                    active=True,
                    group_admin=user.id,
                )
                user_group.groups_to_users.append(user)
                db.session.add(user_group)
                db.session.commit()

    @classmethod
    def update_user_group(cls, user_group_name=):
        pass

    @classmethod
    def delete_user_group(cls, id):
        db.session.delete(cls._find_user_group(id=id))
        db.session.commit()


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
        cls._find_user(phone=phone, active=active).first()

    @classmethod
    def create_user(cls, phone, fname=None, lname=None, active=True, role=USER_ROLE):
        if not cls.read_user(phone):
            db.session.add(cls(phone=phone, fname=fname, lname=lname, active=active, role=role))
            db.session.commit()

    @classmethod
    def update_user(cls, user):
       if not isinstance(user, cls):
            raise TypeError('User.update_user.user needs to be type User')
        try:
            db.session.commit(user)
        except Exception as e:
            return e

    @classmethod
    def delete_user(cls, phone, active=True):
        db.session.delete(cls.read_user(phone=phone, active=active))
        db.session.commit()


class Message(Base):
    __tablename__ = 'message'

    sms_message_sid = db.Column(db.String(160), nullable=False, primary_key=True)
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
        db.session.add(
            cls(
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
        )
        db.session.commit()

    @classmethod
    def delete_message(cls, sms_message_sid):
        db.session.delete(cls._find_message(sms_message_sid=sms_message_sid))
        db.session.commit()

