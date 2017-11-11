# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated

import datetime
import hashlib
import decimal
import json
import base.common.orm

import src.common as common

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

            if following_only:
                common.add_to_timeline(self.auth_user, "FOLLOWTOURNAMENT", {"tournament": t.id, "text":
                    "User {} is following tournament \"{}\"".format(self.auth_user.user.display_name(), t.name)})
            else:
                common.add_to_timeline(self.auth_user, "ATTENDINGTOURNAMENT", {"tournament": t.id, "text":
                    "User {} attend to participante tournament \"{}\"".format(self.auth_user.user.display_name(), t.name)})

            _session.commit()

            return self.ok({'id_tournament': id_tournament,
                            'image': hashlib.md5(self.auth_user.username.encode()).hexdigest() if
                            self.auth_user.user.have_picture else 'avatar'
                            })
        else:
            if following_only != u2t.following_only:
                u2t.following_only = following_only

                if following_only:
                    common.add_to_timeline(self.auth_user, "FOLLOWTOURNAMENT", {"tournament": t.id, "text":
                        "User {} is following tournament \"{}\"".format(self.auth_user.user.display_name(), t.name)})
                else:
                    common.add_to_timeline(self.auth_user, "ATTENDINGTOURNAMENT", {"tournament": t.id, "text":
                        "User {} attend to participante tournament \"{}\"".format(self.auth_user.user.display_name(),
                                                                                  t.name)})

                _session.commit()

                return self.ok({'id_tournament': id_tournament,
                                'image': hashlib.md5(self.auth_user.username.encode()).hexdigest() if
                                self.auth_user.user.have_picture else 'avatar'
                                })

                return self.ok("ok")


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

            common.add_to_timeline(self.auth_user, "UNFOLLOWTOURNAMENT", {"tournament": t.id, "text":
                "User {} stop following tournament \"{}\"".format(self.auth_user.user.display_name(), t.name)})

            _session.commit()

        return self.ok({"status":"ok", "id_tournament":id_tournament})




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
        {'name': 'logo', 'type': str, 'doc': 'logo'},
        {'name': 'background_image', 'type': str, 'doc': 'background_image'},

    )
    def put(self, name, location, lat, lon, website, date_start, date_end, price, cost, max_participants, id_region, logo, background_image):

        oTournament, _session = base.common.orm.get_orm_model('tournaments')
        oRegion, _session = base.common.orm.get_orm_model('regions')

        from base.common.sequencer import sequencer

        r = _session.query(oTournament).filter(oTournament.name == name, oTournament.date_start == date_start ).one_or_none()
        if r:
            return self.ok({"id": r.id})

        reg = _session.query(oRegion).filter(oRegion.id == id_region ).one_or_none()

        if not reg:
            return self.error("invalid region")

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
            id_region=id_region,
            logo = logo,
            background_image = background_image
        )
        _session.add(tournament)

        common.add_to_timeline(None, "NEWTOURNAMENT", {"tournament": tid, "logo": logo, "background": background_image, "text":
            "New tournament {} at {} added / region: {}".format(name, location, reg.name_ger)})

        _session.commit()


        return self.ok({"id":tid})

    @authenticated()
    def get(self):

        '''
cat tournament | awk -F ',' '{print "curl -X PUT \"http://tourgolfer.digitalcube.rs:8802/api/tournaments?name="$1"&location="$2"&lat="$3"&lon="$4"&website="$7"&date_start="$5"&date_end="$6"&price="$8"&cost="$9"&max_participants="$10"&id_region=r000004xcY\""}' | bash
        '''

        oRegion, _session = base.common.orm.get_orm_model('regions')
        oUser, _session = base.common.orm.get_orm_model('users')
        oTournament, _session = base.common.orm.get_orm_model('tournaments')
        oUser2Tournament, _session = base.common.orm.get_orm_model('user_2_tournament')

        result = []

        for t in _session.query(oTournament).filter().all():

            status = "non_following"

            x1=t.id

            ut = _session.query(oUser2Tournament).filter(oUser2Tournament.id_user == self.auth_user.id, oUser2Tournament.id_tournament == t.id).one_or_none()

            if ut:
                status = "following" if ut.following_only else "participating"

            ut = _session.query(oUser2Tournament).filter(oUser2Tournament.id_tournament == t.id).all()

            participants = []
            nr_participants = 0
            for p in ut:

                u = _session.query(oUser).filter(oUser.id == p.id_user).one()
                picture = 'avatar'
                if u.have_picture:
                    picture = hashlib.md5(u.auth_user.username.encode()).hexdigest()

                participants.append(picture)
                nr_participants+=1

            print("PPP", participants)

            print("PPP",participants,str(t.date_start),t.name.replace('%20',' '))
            reg = _session.query(oRegion).filter(oRegion.id == t.id_region).one()
            result.append(

                {"id":t.id,
                 "participants": participants,
                 "name": t.name.replace('%20',' ') if t.name else 'N/A',
                 "location": t.location.replace('%20', ' ') if t.location else 'N/A',
                 "coordinates": {"lat": float(t.lat), "lon": float(t.lon)},
                 "website": t.website,
                 "date_start": str(t.date_start),
                 "date_end": str(t.date_end),
                 "price": float(t.price),
                 "cost": float(t.cost),
                 "max_participants": t.max_participants,
                 "free_participants": t.max_participants - nr_participants,
                 "region": {
                     "id": t.id_region,
                     "name_ita": reg.name_ita.replace('%20',' ') if reg.name_ita else '',
                     "name_ger": reg.name_ger.replace('%20',' ') if reg.name_ger else '',
                 },
                 "status": status
                 }

            )

        return self.ok({"tournaments": result})
