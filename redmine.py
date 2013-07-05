import requests
import settings


def get_issues(project):

    api_issues = settings.http_url+'/projects/'+project+'/issues.json?set_filter=1&f[]=status_id&op[status_id]=*&f[]=is_private&op[is_private]=%3D&v[is_private][]=0'
    api_auth = (settings.http_user, settings.http_pass)

    api_header = {'X-Redmine-API-Key': settings.api_key}

    offset = 0
    offset_add = 100
    total_count = 1

    issues = []

    # retrieve issues
    while offset < total_count:
        
        url = api_issues+'&offset='+str(offset)+'&limit='+str(offset_add)
        result = requests.get(url, auth=api_auth, verify=False, 
                            headers=api_header).json()
    
        for issue in result['issues']:
            issues.append(issue)

        offset = result['offset']
        total_count = result['total_count']

        if not total_count:
            break

        offset += offset_add

    return issues

