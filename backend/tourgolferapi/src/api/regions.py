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
    URI='/regions',
)
class Regions(Base):
    @params(
        {'name': 'name_ger', 'type': str, 'doc': 'name of region (german)'},
        {'name': 'name_ita', 'type': str, 'doc': 'name of region (italian)'},
    )
    def put(self,name_ger, name_ita):


        '''

cat region | awk -F ',' '{print "curl -X PUT \"http://tourgolfer.digitalcube.rs:8802/api/regions?name_ita="$3"&name_ger="$2"\""}' | bash

        '''
        oRegion, _session = base.common.orm.get_orm_model('regions')

        r = _session.query(oRegion).filter(oRegion.name_ger == name_ger).one_or_none()
        if r:
            return self.ok({"id": r.id})

        from base.common.sequencer import sequencer
        rid = sequencer().new('r')

        region = oRegion(rid, name_ger, name_ita)
        _session.add(region)
        _session.commit()


        return self.ok({"id":rid})

    def get(self):
        oRegion, _session = base.common.orm.get_orm_model('regions')

        result = []

        for r in _session.query(oRegion).filter().all():
            result.append({"id": r.id,
                           "name_ita": r.name_ita,
                           "name_ger": r.name_ger})

        return self.ok({'regions': result})
