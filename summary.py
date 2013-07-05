import settings
import redmine
import os

from jinja2 import Environment, FileSystemLoader

project = 'backspace'

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(templates_dir),
                  extensions=['jinja2.ext.loopcontrols'])

template = env.get_template('summary.jinja2')
print template.render(issues=redmine.get_issues(project))
