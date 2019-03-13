#!/usr/bin/env python
#usage:python wikiscript.py <USERNAME>

import requests
import sys
import json
from dateutil import parser
from datetime import datetime, timedelta

def query_user(user):
    res=requests.get("https://en.wikipedia.org/w/api.php?action=query&format=json&list=usercontribs&ucuser="+user+"&uclimit=1&ucdir=older")
    return json.loads(res.text)['query']['usercontribs'][0]['timestamp']

def test_user_time(user):
    timestamp = query_user(user)
    past = parser.parse(timestamp).replace(tzinfo=None)
    present = datetime.now().replace(tzinfo=None)
    diff=present-past
    return diff.days<30

if __name__ == '__main__':
    user=sys.argv[1]
    print((query_user(user)))
    print((test_user_time(user)))
