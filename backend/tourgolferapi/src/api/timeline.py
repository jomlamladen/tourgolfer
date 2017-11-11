# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

from sqlalchemy import desc

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

        followers = set()

        for f in _session.query(oFollowers).filter(oFollowers.id_user == self.auth_user.id).all():
            followers.add(f.id_user)

        res = []
        for t in _session.query(oTimeline).order_by(desc(oTimeline.id)).all():
            j = json.loads(t.json_data)
            if t.id_user in followers or not t.id_user:
                res.append({'action': t.action,
                            'time': str(t.timestamp),
                            'text': j['text']})

        return self.ok({'timeline': res})
