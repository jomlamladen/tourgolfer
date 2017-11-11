# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

import datetime
import decimal
import json

import base.common.orm


# @authenticated()  # if every http method has to be authenticated
@api(
    URI='/users',
)
class Users(Base):

    @params(  # if you want to add params
        {'name': 'id_region', 'type': str, 'doc': 'id of region', 'required': False},
    )
    @authenticated()

    def get(self, id_region):
        import hashlib

        oUser, _session = base.common.orm.get_orm_model('users')
        oFollower, _session = base.common.orm.get_orm_model('followers')

        users = []

        for u in _session.query(oUser).all():

            f = _session.query(oFollower).filter(oFollower.id_user == self.auth_user.id,
                                                 oFollower.id_following == u.id).one_or_none()

            users.append({
                "id":u.id,
                "first_name": u.first_name.replace('%20', ' ') if u.first_name else '',
                "last_name": u.last_name.replace('%20', ' ') if u.last_name else '',
                "email": u.auth_user.username,
                "following": f is not None,
                "image": "{}".format(hashlib.md5(u.auth_user.username.encode()).hexdigest()) if u.have_picture else 'avatar'
            })

        return self.ok({'users': users})
