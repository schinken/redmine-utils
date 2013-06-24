import requests
import settings

import dateutil.parser
from datetime import datetime, timedelta

lastrun = timedelta(days=7)

project = 'backspace'
 
users_existing = []
users_ingroup = []
 
api_issues = settings.http_url+'/projects/'+project+'/issues.json?status_id=*'

api_header = {'X-Redmine-API-Key': settings.api_key}
api_auth = (settings.http_user, settings.http_pass)


# retrieve issues
issues = []
datefields = ['created_on', 'updated_on', 'closed_on']

offset = 0
offset_add = 100
total_count = 1

while offset < total_count:
    
    url = api_issues+'&offset='+str(offset)+'&limit='+str(offset_add)
    result = requests.get(url, auth=api_auth, headers=api_header,
                          verify=False).json()
 
    for issue in result['issues']:

        for field in datefields:
            if field in issue:
                issue[field] = dateutil.parser.parse(issue[field])

        issues.append(issue)

    offset = result['offset']
    total_count = result['total_count']

    if not total_count:
        break

    offset += offset_add


print issues

