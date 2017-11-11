# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

from sqlalchemy import desc
import hashlib

import src.common as common

import datetime
import decimal
import json

import base.common.orm


# @authenticated()  # if every http method has to be authenticated
@api(
    URI='/timeline',
)
class Status(Base):
    @authenticated()
    def get(self):

        oTimeline, _session = base.common.orm.get_orm_model('timeline')
        oFollowers, _session = base.common.orm.get_orm_model('followers')
        oUser, _session = base.common.orm.get_orm_model('users')

        followers = set()

        for f in _session.query(oFollowers).filter(oFollowers.id_user == self.auth_user.id).all():
            followers.add(f.id_user)

        res = []
        for t in _session.query(oTimeline).order_by(desc(oTimeline.id)).all():
            j = json.loads(t.json_data)
            if t.id_user in followers or not t.id_user:

                user = _session.query(oUser).filter(oUser.id == t.id_user).one_or_none()

                if user:
                    user = {
                        'id': user.id,
                        'first_name': user.first_name.replace('%20', ' ') if user.first_name else '',
                        'last_name': user.last_name.replace('%20', ' ') if user.last_name else '',
                        'image': hashlib.md5(user.auth_user.username.encode()).hexdigest() if user.have_picture else 'avatar'
                    }

                res.append({'action': t.action,
                            'user': user,
                            'id_user': t.id_user,
                            'time': str(t.timestamp),
                            'text': j['text'].replace('%20',' ')
                            })

        return self.ok({'timeline': res})
