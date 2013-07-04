import requests
import settings
import mwclient
import os

from jinja2 import Environment, FileSystemLoader

from time import mktime
from datetime import datetime
from dateutil import parser
from collections import defaultdict

project = 'backspace'

api_issues = settings.http_url+'/projects/'+project+'/issues.json?set_filter=1&f[]=status_id&op[status_id]=*&f[]=is_private&op[is_private]=%3D&v[is_private][]=0'
api_auth = (settings.http_user, settings.http_pass)

api_header = {'X-Redmine-API-Key': settings.api_key}

# We explicitly don't use the API key here to access the tickets, to avoid
# retrieving private tickets. theres no field to indicate if its private
# or not

wiki_time = datetime.now()
wiki_update = False

site = mwclient.Site('www.hackerspace-bamberg.de', path='/')
site.login(settings.mediawiki_user, settings.mediawiki_pass)

page = site.Pages[settings.mediawiki_page]
for rev in page.revisions(limit=1):
    wiki_time = datetime.fromtimestamp(mktime(rev['timestamp']))
    break

offset = 0
offset_add = 100
total_count = 1

issues_by_category = defaultdict(list)

# retrieve issues
while offset < total_count:
    
    url = api_issues+'&offset='+str(offset)+'&limit='+str(offset_add)
    result = requests.get(url, auth=api_auth, verify=False, 
                          headers=api_header).json()
 
    for issue in result['issues']:

        if 'closed_on' in issue:
            continue

        if parser.parse(issue['updated_on']).replace(tzinfo=None) > wiki_time:
            wiki_update = True

        tracker = issue['tracker']['name']
        issues_by_category[tracker].append(issue)

    offset = result['offset']
    total_count = result['total_count']

    if not total_count:
        break

    offset += offset_add


templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))

def format_redmine_date(value):
    dt = parser.parse(value)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

env.filters['redminedate'] = format_redmine_date


if wiki_update:

    print "Updated mediawiki"

    template = env.get_template('mediawiki.jinja2')
    tpl_result = template.render(issues=issues_by_category)
    page.save(tpl_result, summary='Ticket changed')

