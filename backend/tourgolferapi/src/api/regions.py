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
    URI='/regions',
)
class Regions(Base):

    def get(self):
        return self.ok({
                        "regions":[{"id":"r00000abc",
                         "name_ita":"Bolzano",
                         "name_ger":"Bozen"
                         },
                        {"id": "r00000abd",
                         "name_ita": "Burgravito",
                         "name_ger": "Burggrafenamt"
                         },
                        ]})
