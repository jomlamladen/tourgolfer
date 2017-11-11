

from tornado import httpclient
import json
import sys


tokens = {}
regions = {}
tournaments = {}
uids ={}


def register_user(username, first_name, last_name, password):

    http_client = httpclient.HTTPClient()
    post_data = {'username': username, 'password': password, 'data': {'first_name': first_name, 'last_name': last_name}}
    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json'}
    req = httpclient.HTTPRequest("http://localhost:8802/user/register", method='POST', body=body, headers=headers)
    res = http_client.fetch(req)

    res = json.loads(res.body.decode('utf-8'))
    return res['token']

    print(res)

def add_tournament(name,
                   location,
                   lat,
                   lon,
                   date_start,
                   date_end,
                   website,
                   price,
                   cost,
                   max_participans,
                   id_region,
                   logo,
                   background_image):

    http_client = httpclient.HTTPClient()
    post_data = {'name': name,
                 'location': location,
                 'lat': lat,
                 'lon': lon,
                 'date_start': date_start,
                 'date_end': date_end,
                 'website': website,
                 'price': price,
                 'cost': cost,
                 'max_participants': max_participans,
                 'id_region': id_region,
                 'logo': logo,
                 'background_image': background_image
                 }

    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json'}
    req = httpclient.HTTPRequest("http://localhost:8802/api/tournaments", method='PUT', body=body, headers=headers)
    res = http_client.fetch(req)

    res = json.loads(res.body.decode('utf-8'))
    print(res)
    return res['id']



def add_region(name_ger, name_ita):
    http_client = httpclient.HTTPClient()
    post_data = {'name_ita': name_ita, 'name_ger': name_ger}
    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json'}
    req = httpclient.HTTPRequest("http://localhost:8802/api/regions", method='PUT', body=body, headers=headers)
    res = http_client.fetch(req)

    res = json.loads(res.body.decode('utf-8'))
    return res['id']





def login_user(username, password):

    http_client = httpclient.HTTPClient()
    post_data = {'username': username, 'password': password}
    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json'}
    req = httpclient.HTTPRequest("http://localhost:8802/user/login", method='POST', body=body, headers=headers)
    res = http_client.fetch(req)

    res = json.loads(res.body.decode('utf-8'))
    return res['token']


def login_or_register(username, first_name, last_name, password):

    try:
        return login_user(username, password)
    except:
        return register_user(username, first_name, last_name, password)

def timeline(for_user):
    tok = tokens[for_user]
    http_client = httpclient.HTTPClient()
    headers = {'Content-Type': 'application/json', 'Authorization': tok}
    req = httpclient.HTTPRequest("http://localhost:8802/api/timeline", method='GET', headers=headers)
    res = http_client.fetch(req)
    res = json.loads(res.body.decode('utf-8'))
    print("timeline for ",for_user)
    for t in res['timeline']:
        print("\t",t['time'], t['text'])


def follow_user(user_who_follow, user_who_is_followed, follow=True):

    print('follow',follow)
    tok = tokens[user_who_follow]
    uid = uids[user_who_is_followed]

    http_client = httpclient.HTTPClient()
    post_data = {'id_following': uid}
    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json', 'Authorization': tok}
    method = 'PUT' if follow else 'DELETE'
    if method=='PUT':
        req = httpclient.HTTPRequest("http://localhost:8802/api/follow", method=method, body=body, headers=headers)
    if method=='DELETE':
        req = httpclient.HTTPRequest("http://localhost:8802/api/follow?id_following={}".format(uid), method=method, headers=headers)

    try:
        res = http_client.fetch(req)

        res = json.loads(res.body.decode('utf-8'))
        print("RRR",res)
    except Exception as e:
        print(e)


def participate_tournament(username, tournament_name_date):

    tok = tokens[username]
    tid = tournaments[tournament_name_date]

    http_client = httpclient.HTTPClient()
    post_data = {'following_only': False}
    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json', 'Authorization': tok}
    req = httpclient.HTTPRequest("http://localhost:8802/api/tournaments/{}".format(tid), method='PUT', body=body, headers=headers)
    res = http_client.fetch(req)

    res = json.loads(res.body.decode('utf-8'))


def list_of_users():
    tok = tokens['igor@digitalcube.rs']

    http_client = httpclient.HTTPClient()
    post_data = {}
    body = json.dumps(post_data)
    headers = {'Content-Type': 'application/json', 'Authorization': tok}
    req = httpclient.HTTPRequest("http://localhost:8802/api/users", method='GET', headers=headers)
    res = http_client.fetch(req)

    res = json.loads(res.body.decode('utf-8'))
    return (res)



import csv





with open("/Users/igorjeremic/Downloads/users", "rt") as f:
    for l in csv.reader(f):
        eml = l[0]
        x = login_or_register(eml, l[1], l[2], '123')
        tokens[eml] = x
        print(x)


for u in list_of_users()['users']:
    uids[u['email']]=u['id']


with open("/Users/igorjeremic/Downloads/regions", "rt") as f:
    for l in csv.reader(f):
        x = add_region(l[0],l[1])
        regions[l[0]] = x

print(regions)


with open('/Users/igorjeremic/Downloads/tournaments', "rt") as f:
    for l in csv.reader(f):
        x = add_tournament(name = l[0],
                           location = l[1],
                           lat=l[2],
                           lon=l[3],
                           date_start=l[4],
                           date_end=l[5],
                           website=l[6],
                           price=l[7],
                           cost=l[8],
                           max_participans=l[9],
                           id_region=regions[l[10]],
                           logo=l[11],
                           background_image=l[12])

        tournaments["{}:{}".format(l[0],l[4])] = x

print(tournaments)
'''
participate_tournament('bjoern@tourgolf.com', 'Funtime:2018-03-29')
follow_user('igor@digitalcube.rs','bjoern@tourgolf.com')
follow_user('igor@digitalcube.rs','bjoern@tourgolf.com',follow=False)
follow_user('igor@digitalcube.rs','lukas.stenico17@gmail.com')
follow_user('lukas.stenico17@gmail.com','mladen@digitalcube.rs')
participate_tournament('mladen@digitalcube.rs', 'Funtime:2018-03-29')
'''

timeline('igor@digitalcube.rs')
timeline('lukas.stenico17@gmail.com')
