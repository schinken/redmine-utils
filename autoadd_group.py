import requests
import json
import settings

group = 15
 
users_existing = []
users_ingroup = []
 
api_user = settings.http_url+'/users.json'
api_group = settings.http_url+'/groups/'+str(group)+'.json?include=users'
api_user_add = settings.http_url+'/groups/'+str(group)+'/users.xml'
 
print api_user, api_group, api_user_add

api_header = {'X-Redmine-API-Key': settings.api_key}
api_auth = (settings.http_user, settings.http_pass)
 
# retrieve users
users = requests.get(api_user, auth=api_auth, headers=api_header).json()
 
for user in users['users']:
    users_existing.append(user['id'])
 
# retrieve users for groups
groups = requests.get(api_group, auth=api_auth,headers=api_header).json()
for user in groups['group']['users']:
    users_ingroup.append(user['id'])
 
# create diff and add users
users_missing = list(set(users_existing) - set(users_ingroup))
for user in users_missing:
 
    print "Adding user", user
    useradd = {'user_id': user}
    result = requests.post(api_user_add, auth=api_auth, data=useradd,
                           headers=api_header)
