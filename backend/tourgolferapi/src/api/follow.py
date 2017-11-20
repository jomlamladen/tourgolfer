# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

import src.common as common

import datetime
import decimal
import json

import base.common.orm


# @authenticated()  # if every http method has to be authenticated
@api(
    URI='/follow',
)
class Follow(Base):
    @authenticated()
    @params(  # if you want to add params
        {'name': 'id_following', 'type': str, 'doc': 'name of tournament'},
    )
    def put(self, id_following):

        oUser, _session = base.common.orm.get_orm_model('users')
        oFollower, _session = base.common.orm.get_orm_model('followers')

        u = _session.query(oUser).filter(oUser.id == id_following).one_or_none()

        if not u:
            return self.error("user with given id don't exists")

        f = _session.query(oFollower).filter(oFollower.id_user == self.auth_user.id, oFollower.id_following == id_following).one_or_none()

        if f:
            return self.error("this user is already in followed")

        follower = oFollower(self.auth_user.id, id_following)
        _session.add(follower)
        common.add_to_timeline(self.auth_user, "FOLLOW", {"target_user": id_following, "text":
            "user {} start following {}".format(self.auth_user.user.display_name(), u.display_name())})
        _session.commit()

        return self.ok({'id': id_following})

    @authenticated()
    @params(  # if you want to add params
        {'name': 'id_following', 'type': str, 'doc': 'name of tournament'},
    )
    def delete(self, id_following):

        oUser, _session = base.common.orm.get_orm_model('users')
        oFollower, _session = base.common.orm.get_orm_model('followers')

        u = _session.query(oUser).filter(oUser.id == id_following).one_or_none()

        if not u:
            return self.error("user with given id don't exists")

        f = _session.query(oFollower).filter(oFollower.id_user == self.auth_user.id, oFollower.id_following == id_following).one_or_none()

        if not f:
            return self.error("this user is not followed")

        _session.query(oFollower).filter(oFollower.id_user == self.auth_user.id,
                                         oFollower.id_following == id_following).delete()

        common.add_to_timeline(self.auth_user, "UNFOLLOW", {"target_user": id_following, "text":
            "user {} stop following {}".format(self.auth_user.user.display_name(), u.display_name())})

        _session.commit()

        return self.ok({'id': id_following})


    @authenticated()
    def get(self):

        oUser, _session = base.common.orm.get_orm_model('users')
        oFollower, _session = base.common.orm.get_orm_model('followers')

        following = []

        for f in _session.query(oFollower).filter(oFollower.id_user == self.auth_user.id).all():

            u = _session.query(oUser).filter(oUser.id == f.id_following).one_or_none()
            if u:
                following.append({'id':f.id_following,
                                  'email': u.auth_user.username,
                                  'first_name': u.first_name,
                                  'last_name': u.last_name,
                                  })

        return self.ok({'following': following})
