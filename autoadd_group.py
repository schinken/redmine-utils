import requests
import settings

# Disable HTTPS verification warnings.
from requests.packages import urllib3
urllib3.disable_warnings()

group = 15
 
users_existing = []
users_ingroup = []
id_to_nick = {}

api_user = settings.http_url+'/users.json?limit=1000'
api_group = settings.http_url+'/groups/'+str(group)+'.json?include=users'
api_user_add = settings.http_url+'/groups/'+str(group)+'/users.xml'

api_header = {'X-Redmine-API-Key': settings.api_key}
api_auth = (settings.http_user, settings.http_pass)
 
# retrieve users
users = requests.get(api_user, auth=api_auth, headers=api_header,
                    verify=False).json()
 
for user in users['users']:
    uid = user['id']
    id_to_nick[uid] = user['login']
    users_existing.append(uid)
    
# include locked users
users = requests.get(api_user + "&status=3", auth=api_auth, headers=api_header,
                    verify=False).json()

for user in users['users']:
    uid = user['id']
    id_to_nick[uid] = user['login']
    users_existing.append(uid)

 
# retrieve users for groups
groups = requests.get(api_group, auth=api_auth,headers=api_header,
                    verify=False).json()
for user in groups['group']['users']:
    users_ingroup.append(user['id'])
 
# create diff and add users
users_missing = list(set(users_existing) - set(users_ingroup))
for user in users_missing:
 
    useradd = {'user_id': user}
    result = requests.post(api_user_add, auth=api_auth, data=useradd,
                           headers=api_header, verify=False)

    print "Adding user_id:", user, " login: ", id_to_nick[user]
