#!/usr/bin/python

import twitter
import string
import os.path
import os
import random
import time
import sys
from   time import gmtime, strftime


# Initialization variables
CONSUMER_KEY        = '8iuJ0lzJHKT8PV9RwqEjQkIZj'
CONSUMER_SECRET     = 'RZj0TRte2nJmWMWePDu85BeYmsVAdQpOAgFNJcTcMbvD0hpmGY'
ACCESS_TOKEN_KEY    = '11635342-7ACgqjPS0ABMrKojWbIrpzZrHmgyXzSW55IFiNAnQ'
ACCESS_TOKEN_SECRET = 'PKYcgDNUV9QiiQ1aeAY7mW72IBRrwVG7s87dLwzuUiLDA'

THRESHOLD = 7*24*60*60 # Keep 7 days worth of tweets


# Connecting to Twitter API
api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET)
api.sleep_on_rate_limit = True


def writeLog(content):
	currenttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	print currenttime + " - " + content




oldtweets = api.GetUserTimeline(count=200)
maxsec = 0
maxid = 0
currid = 0
currsec = 0
for t in oldtweets:
	created = t.created_at_in_seconds
	currsec = created
	currid = t.id
	if created<THRESHOLD:
		maxsec = created
		maxid = t.id
		break
if maxid == 0:
	maxid = currid
	maxsec = currsec

writeLog("Earliest to keep " + str(maxid) + " [" + strftime("%Y-%m-%d %H:%M:%S", gmtime(maxsec)) + "]")

oldtweets = api.GetUserTimeline(count=200, max_id=maxid, trim_user=True)
for t in oldtweets:
	api.DestroyStatus(t.id)
	writeLog("Deleted ID " + str(t.id) + " [" + t.created_at + "]")
writeLog("TICK")


