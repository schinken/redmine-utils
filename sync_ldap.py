import requests
import settings
import hashlib
import json
import time
import ldap
import sys

# Disable HTTPS verification warnings.
from requests.packages import urllib3
urllib3.disable_warnings()

api_user = settings.http_url+'/users.json'
api_header = {
    'X-Redmine-API-Key': settings.api_key,
    'Content-Type': 'application/json'
}

api_auth = (settings.http_user, settings.http_pass)

con = ldap.initialize(settings.ldap_uri)
con.protocol_version = ldap.VERSION3

con.bind(settings.ldap_dn, settings.ldap_pw)

# retrieve users
existing_users = []
users = requests.get(api_user + '?limit=1000', auth=api_auth, headers=api_header,
                    verify=False).json()
 
for user in users['users']:
    existing_users.append(user['login'])
    
# include locked users
users = requests.get(api_user + '?limit=1000&status=3', auth=api_auth, headers=api_header,
                    verify=False).json()

for user in users['users']:
    existing_users.append(user['login'])

users = con.search_s('ou=member,dc=backspace', ldap.SCOPE_SUBTREE, '(&(objectClass=backspaceMember)(serviceEnabled=redmine))', ['uid', 'mlAddress', 'alternateEmail'])
for user in users:
    uid = user[1]['uid'][0]

    if 'mlAddress' in user[1]:
        mail = user[1]['mlAddress'][0]
    else:
        mail = user[1]['alternateEmail'][0]

    if uid in existing_users:
        continue

    useradd = {
        "user": {
            "login": uid,
            "firstname": uid,
            "lastname": "backspace",
            "mail": mail,
            "auth_source_id": 3
        }
    }

    print "Adding user %s to Redmine" % (uid,)
    result = requests.post(api_user, auth=api_auth, data=json.dumps(useradd),
                           headers=api_header, verify=False)

