import base.common.orm

import json

def add_to_timeline(user, action, json_data):

    oTimeline, _session = base.common.orm.get_orm_model('timeline')
    _session.add( oTimeline(action, json.dumps(json_data), user.id if user else None))

def add_to_timeline_idu(id_user, action, json_data):

    oTimeline, _session = base.common.orm.get_orm_model('timeline')
    _session.add( oTimeline(action, json.dumps(json_data), id_user))
