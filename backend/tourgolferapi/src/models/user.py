import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text, CHAR, Numeric, Date
from sqlalchemy.orm import relationship
import base.common.orm
from sqlalchemy import UniqueConstraint


class Region(base.common.orm.sql_base):

    __tablename__ = 'regions'

    id = Column(CHAR(10), primary_key=True)
    name_ger = Column(String(32), unique=True, nullable=False)
    name_ita = Column(String(32), unique=True, nullable=False)

    def __init__(self, id, name_ger, name_ita):
        self.id = id
        self.name_ger = name_ger
        self.name_ita = name_ita


class Tournament(base.common.orm.sql_base):

    __tablename__ = 'tournaments'

    id = Column(CHAR(10), primary_key=True)
    name = Column(String(128), index=False, nullable=False)
    location = Column(String(128), index=False, nullable=False)
    lat = Column(Numeric(16, 12), index=False, nullable=False)
    lon = Column(Numeric(16, 12), index=False, nullable=False)
    date_start = Column(Date, index=False, nullable=False)
    date_end = Column(Date, index=False, nullable=False)
    website = Column(String(255), index=False, nullable=False)
    price = Column(Numeric(12, 2), index=False, nullable=False)
    cost = Column(Numeric(12, 2), index=False, nullable=False)
    max_participants = Column(Integer, index=False, nullable=False)
    id_region = Column(CHAR(10), index=True, nullable=False)

    def __init__(self, id, name, location, lat, lon, date_start, date_end, website, price, cost, max_participants, id_region):
        self.id = id
        self.name = name
        self.location = location
        self.lat = lat
        self.lon = lon
        self.date_start = date_start
        self.date_end = date_end
        self.website = website
        self.price = price
        self.cost = cost
        self.max_participants = max_participants
        self.id_region = id_region

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

    id_user = Column(CHAR(10), ForeignKey(User.id))
    id_following = Column(CHAR(10), ForeignKey(User.id))

    uix_1 = UniqueConstraint('id_following', 'id_user', name='uix_1')

    def __init__(self, id_user, id_following):
        self.id_following = id_following
        self.id_user = id_user



def main():
    pass

if __name__ == '__main__':

    main()

    '''
    http://tourgolfer.digitalcube.rs:8802/user/register?username=igor@digitalcube.rs&password=123&data={"first_name":"Igor","last_name":"Jeremic"}
    http://tourgolfer.digitalcube.rs:8802/user/register?username=milicevicdj@gmail.com&password=123&data={"first_name":"Mladen","last_name":"Milicevic"}
    http://tourgolfer.digitalcube.rs:8802/user/register?username=anjan8@gmail.com&password=123&data={"first_name":"Anjan","last_name":"Karmakar"}
    http://tourgolfer.digitalcube.rs:8802/user/register?username=lukas.stenico17@gmail.com&password=123&data={"first_name":"Lukas","last_name":"Stenico"}
    
    '''
