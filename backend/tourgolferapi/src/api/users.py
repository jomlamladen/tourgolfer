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
    def get(self, id_region):

        oUser, _session = base.common.orm.get_orm_model('users')

        print(oUser)

        return self.ok()
