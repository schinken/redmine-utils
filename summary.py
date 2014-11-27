# -*- coding: utf-8 -*-
import settings
import smtplib
import redmine
import os
import datetime

from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

# Disable HTTPS verification warnings.
from requests.packages import urllib3
urllib3.disable_warnings()

project = 'backspace'

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(templates_dir),
                  extensions=['jinja2.ext.loopcontrols'])

template = env.get_template('summary.jinja2')
mail = template.render(issues=redmine.get_issues(project),
                       week_ago=str(datetime.date.today()-datetime.timedelta(7)))


# Prepare MIME Mail
msg = MIMEText(mail.encode('utf-8'), 'plain', 'utf-8')
msg['Subject'] = settings.summary_subject
msg['From'] = settings.summary_from
msg['To'] = settings.summary_to

if settings.summary_reference:
    msg['References'] = settings.summary_reference

# Actually send mail

smtp = smtplib.SMTP(settings.summary_host, settings.summary_port)
smtp.sendmail(settings.summary_from, [settings.summary_to], msg.as_string())
smtp.quit()
