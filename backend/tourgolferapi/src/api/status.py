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
    URI='/status',
)
class Status(Base):
    @authenticated()
    @params(  # if you want to add params
        {'name': 'status', 'type': str, 'doc': 'user status'},
    )
    def put(self, status):

        oUser, _session = base.common.orm.get_orm_model('users')

        common.add_to_timeline(self.auth_user, "SETSTATUS", {"status": status, "text":
            "user {} set status to \"{}\"".format(self.auth_user.user.display_name(), status)})
        _session.commit()

        return self.ok()
