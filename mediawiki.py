import settings
import mwclient
import redmine
import os

from jinja2 import Environment, FileSystemLoader

from time import mktime
from datetime import datetime
from dateutil import parser
from collections import defaultdict

project = 'backspace'

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
for issue in redmine.get_issues(project):

    if parser.parse(issue['updated_on']).replace(tzinfo=None) > wiki_time:
        wiki_update = True

    if 'closed_on' in issue:
        continue

    tracker = issue['tracker']['name']
    issues_by_category[tracker].append(issue)


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

