# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

import datetime
import decimal
import json
import base.common.orm


@api(
    URI='/tournaments/:id_tournament',
)
class Torunament(Base):
    @params(
        {'name': 'id_tournament', 'type': str, 'doc': 'id of tournament'},
        {'name': 'following_only', 'type': bool, 'doc': 'true if user is only follower'},
    )
    @authenticated()
    def put(self, id_tournament, following_only):
        print(id_tournament, self.auth_user.id)

        oTournament, _session = base.common.orm.get_orm_model('tournaments')
        oUser2Tournament, _session = base.common.orm.get_orm_model('user_2_tournament')

        t = _session.query(oTournament).filter(oTournament.id == id_tournament).one_or_none()

        if not t:
            return self.error("tournament with given id does not exists in database")

        u2t = _session.query(oUser2Tournament).filter(oUser2Tournament.id_user == self.auth_user.id, oUser2Tournament.id_tournament == id_tournament).one_or_none()

        if not u2t:
            u2t = oUser2Tournament(self.auth_user.id, id_tournament, following_only)
            _session.add(u2t)
            _session.commit()

            return self.ok("OK added")
        else:
            if following_only != u2t.following_only:
                u2t.following_only = following_only
                _session.commit()

                return self.ok("OK changed")


        return self.ok("OK already here")

    @params(
        {'name': 'id_tournament', 'type': str, 'doc': 'id of tournament'},
    )
    @authenticated()
    def delete(self, id_tournament):

        oTournament, _session = base.common.orm.get_orm_model('tournaments')
        oUser2Tournament, _session = base.common.orm.get_orm_model('user_2_tournament')

        t = _session.query(oTournament).filter(oTournament.id == id_tournament).one_or_none()

        if not t:
            return self.error("tournament with given id does not exists in database")

        u2t = _session.query(oUser2Tournament).filter(oUser2Tournament.id_user == self.auth_user.id, oUser2Tournament.id_tournament == id_tournament).one_or_none()

        if not u2t:
            return self.error("there is no user assigned to tournament")
        else:
            _session.query(oUser2Tournament).filter(oUser2Tournament.id_user == self.auth_user.id,
                                                          oUser2Tournament.id_tournament == id_tournament).delete()
            _session.commit()

        return self.ok("OK")




# @authenticated()  # if every http method has to be authenticated
@api(
    URI='/tournaments',
)
class Torunaments(Base):
    @params(  # if you want to add params
        {'name': 'name', 'type': str, 'doc': 'name of tournament'},
        {'name': 'location', 'type': str, 'doc': 'name of tournament'},
        {'name': 'lat', 'type': float, 'doc': 'location - latitude'},
        {'name': 'lon', 'type': float, 'doc': 'location - longitude'},
        {'name': 'website', 'type': str, 'doc': 'name of tournament'},
        {'name': 'date_start', 'type': datetime, 'doc': 'start date of tournament'},
        {'name': 'date_end', 'type': datetime, 'doc': 'end date of tournament'},
        {'name': 'price', 'type': str, 'doc': 'price of tournament'},
        {'name': 'cost', 'type': str, 'doc': 'cost of tournament'},
        {'name': 'max_participants', 'type': str, 'doc': 'max participants of tournament'},
        {'name': 'id_region', 'type': str, 'doc': 'id_region'},

    )
    def put(self, name, location, lat, lon, website, date_start, date_end, price, cost, max_participants, id_region):

        oTournament, _session = base.common.orm.get_orm_model('tournaments')

        from base.common.sequencer import sequencer

        tid = sequencer().new('t')

        tournament = oTournament(

            id=tid,
            name = name,
            location=location,
            lat=lat,
            lon=lon,
            date_start=date_start,
            date_end=date_end,
            website=website,
            price=price,
            cost=cost,
            max_participants=max_participants,
            id_region=id_region
        )
        _session.add(tournament)
        _session.commit()


        return self.ok({"id":tid})

    @authenticated()
    def get(self):

        '''

cat tournament | awk -F ',' '{print "curl -X PUT \"http://tourgolfer.digitalcube.rs:8802/api/tournaments?name="$1"&location="$2"&lat="$3"&lon="$4"&website="$7"&date_start="$5"&date_end="$6"&price="$8"&cost="$9"&max_participants="$10"&id_region=r000002He0\""}' | bash

        '''

        oTournament, _session = base.common.orm.get_orm_model('tournaments')
        oUser2Tournament, _session = base.common.orm.get_orm_model('user_2_tournament')

        result = []

        for t in _session.query(oTournament).filter().all():

            status = "non_following"

            x1=t.id

            ut = _session.query(oUser2Tournament).filter(oUser2Tournament.id_user == self.auth_user.id, oUser2Tournament.id_tournament == t.id).one_or_none()

            if ut:
                status = "following" if ut.following_only else "participating"

            result.append(

                {"id":t.id,
                 "name": t.name,
                 "location": "Kellerlahne 3",
                 "coordinates": {"lat": 46.4912183, "lon": 11.3053763},
                 "website": "http://www.golfclubpasseier.com/de/home.php,",
                 "start_date": "2018-03-29",
                 "end_date": "2018-03-29",
                 "price": 0,
                 "cost": 0,
                 "max_participants": 10,
                 "free_participants": 3,
                 "region": {
                     "id": "r00000abc",
                     "name_ita": "Bolzano",
                     "name_ger": "Bozen"
                 },
                 "status": status
                 }

            )

        return self.ok({"tournaments": result})


    def old_get(self):
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
