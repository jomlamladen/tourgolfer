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
    URI='/tournaments',
)
class Torunament(Base):
    @params(  # if you want to add params
        {'name': 'name', 'type': str, 'doc': 'name of tournament'},
        {'name': 'lat', 'type': str, 'doc': 'location - latitude'},
        {'name': 'lon', 'type': str, 'doc': 'location - longitude'},
        {'name': 'www', 'type': str, 'doc': 'name of tournament'},

    )
    def put(self, name, lat, lon, www):
        return self.ok({"id":"mocked"})

    def get(self):
        return self.ok(


            {
                "tournaments":
                    [
                        {"name": "Tournament 1",
                         "location": "Kellerlahne 3",
                         "coordinates": {"lat":46.4912183,"lon":11.3053763},
                         "website": "http://www.golfclubpasseier.com/de/home.php,",
                         "start_date": "2018-03-29",
                         "end_date": "2018-03-29",
                         "price": 0,
                         "cost": 0,
                         "max_participants": 10,
                         "free_participants": 3,
                         "region": {
                             "id":"r00000abc",
                             "name_ita":"Bolzano",
                             "name_ger":"Bozen"
                             }
                         },

                        {"name": "Tournament 2",
                         "location": "Sparbeggweg",
                         "coordinates": {"lat":46.4912183,"lon":11.3053763},
                         "website": "http://www.golfclubpasseier.com/de/home.php,",
                         "start_date": "2018-04-21",
                         "end_date": "2018-04-21",
                         "price": 100,
                         "cost": 10000,
                         "max_participants": 50,
                         "free_participants": 15,
                         "region": {
                             "id": "r00000abc",
                             "name_ita": "Bolzano",
                             "name_ger": "Bozen"
                         }
                         },
                    ],



            }

        )
