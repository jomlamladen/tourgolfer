# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

import datetime
import decimal
import json


# @authenticated()  # if every http method has to be authenticated
@api(
    URI='/follow',
)
class Torunament(Base):
    @authenticated()
    @params(  # if you want to add params
        {'name': 'id_following', 'type': str, 'doc': 'name of tournament'},
    )
    def put(self, id_follower):
        return self.ok({"id":"mocked"})

    @authenticated()
    def get(self):
        return self.ok({"I'm following":[1,2,3]})
