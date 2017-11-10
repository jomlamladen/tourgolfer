import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text, CHAR, Numeric, Date
from sqlalchemy.orm import relationship
import base.common.orm


class Region(base.common.orm.sql_base):

    __tablename__ = 'regions'

    id = Column(CHAR(10), primary_key=True)
    name_ger = Column(String(32), unique=True, nullable=False)
    name_ita = Column(String(32), unique=True, nullable=False)


class Tournament(base.common.orm.sql_base):

    __tablename__ = 'tournaments'

    id = Column(CHAR(10), primary_key=True)
    location = Column(String(128), index=False, nullable=False)
    lat = Column(Numeric(10, 6), index=False, nullable=False)
    lon = Column(Numeric(10, 6), index=False, nullable=False)
    date_start = Column(Date, index=False, nullable=False)
    date_end = Column(Date, index=False, nullable=False)
    website = Column(String(255), index=False, nullable=False)
    price = Column(Numeric(12, 2), index=False, nullable=False)
    cost = Column(Numeric(12, 2), index=False, nullable=False)
    max_participants = Column(Integer, index=False, nullable=False)
    id_region = Column(CHAR(10), index=True, nullable=False)

class AuthUser(base.common.orm.sql_base):

    __tablename__ = 'auth_users'

    id = Column(CHAR(10), primary_key=True)
    username = Column(String(64), index=True, nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    role_flags = Column(Integer, index=True, nullable=False)
    active = Column(Boolean, index=True, nullable=False, default=False)
    created = Column(DateTime, nullable=False, default=datetime.datetime.now())
    user = relationship('User', uselist=False, back_populates='auth_user')

    def __init__(self, _id, username, password, role_flags=1, active=False):

        self.id = _id
        self.username = username
        self.password = password
        self.role_flags = role_flags
        self.active = active
        self.created = datetime.datetime.now()


class User(base.common.orm.sql_base):

    __tablename__ = 'users'

    id = Column(CHAR(10), ForeignKey(AuthUser.id), primary_key=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    data = Column(Text)
    auth_user = relationship("AuthUser", back_populates="user")

    def __init__(self, id_user, first_name, last_name, data):

        self.id = id_user
        self.first_name = first_name
        self.last_name = last_name
        self.data = data


class Followers(base.common.orm.sql_base):

    __tablename__ = 'followers'

    id = Column(Integer, primary_key=True, autoincrement=True)

    id_following = Column(CHAR(10), ForeignKey(User.id))
    id_followed = Column(CHAR(10), ForeignKey(User.id))

    def __init__(self, id_following, id_followed):
        self.id_following = id_following
        self.id_followed = id_followed



def main():
    pass

if __name__ == '__main__':

    main()

    '''
    http://localhost:8802/user/register?username=igor@digitalcube.rs&password=123&data={}
    http://localhost:8802/user/register?username=milicevicdj@gmail.com&password=123&data={}
    http://localhost:8802/user/register?username=anjan8@gmail.com&password=123&data={}
    http://localhost:8802/user/register?username=lukas.stenico17@gmail.com&password=123&data={}
    
    '''
