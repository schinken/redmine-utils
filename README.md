# Redmine-Utils

Due to the lack of some basics in redmine here are some external helper tools which we run as cronjob at hackerspace-bamberg.de

## Installation

At first you have to clone the repository at the location you want
````bash
cd /your/cool/location
git clone https://github.com/schinken/redmine-utils.git
````

If you want, you can use an virtualenv to run these scripts (optional)
````bash
virtualenv env
source ./env/bin/activate
````

And install the requirements:
````bash
pip install -r requirements.txt
````

## autoadd_group

This script adds all your users to a specific group if they're not already in it

## mediawiki

Exports all your done and undone tickets to a mediawiki page. In our case its http://hackerspace-bamberg.de/Todo and http://hackerspace-bamberg.de/Todo:Closed

You can modify the look by adjusting templates inside the templates/ directory

## summary

Mails an Ticket summary with open tickets and closed tickets since the last mail to your destination. In our case a weekly summary of tickets closed is mailed to our mailing list

## sync_ldap

Syncs your users to your redmine instance by creating it through the REST-API (auth_source_id = 3 (this is our LDAP ID in Redmine, may differ on your system))
