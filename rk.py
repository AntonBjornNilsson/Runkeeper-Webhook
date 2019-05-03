import urllib2
import urllib
import json
import math
import requests
import operator

webhook ="""
YOUR WEBHOOK URL HERE
"""
listing = {
    'Friend1' : "https://runkeeper.com/user/Friend1/fitnessReportsData",
    'Friend2' : "https://runkeeper.com/user/Friend2/fitnessReportsData",
    'Friend3' : "https://runkeeper.com/user/Friend3/fitnessReportsData",
    'Friend4' : "https://runkeeper.com/user/Friend4/fitnessReportsData"
}

params = ( # note, needs to be dynamic
    'startDate=2-Apr-2019&endDate=2-May-2019&timeframeOption=LAST_30_DAYS&chartTimeBuckets=WEEK&reportConfigJson=%7B%22totalBoxes%22%3A%7B%22TOTAL_DISTANCE%22%3A%7B%22field%22%3A%22TOTAL_DISTANCE%22%7D%7D%2C%22charts%22%3A%7B%22chart1%22%3A%7B%22field%22%3A%22TOTAL_DISTANCE%22%2C%22stack%22%3A%22true%22%7D%7D%7D'
)

method = "POST"
    # create a handler. you can specify different handlers here (file uploads etc)
    # but we go for the default
handler = urllib2.HTTPHandler()
    # create an openerdirector instance
opener = urllib2.build_opener(handler)



def get_this_week_from_URL(URL):
    data = None
    request = urllib2.Request(URL, params)
    request.get_method = lambda: method
    # try it; don't forget to catch the result
    try:
        connection = opener.open(request)

    except urllib2.HTTPError,e:
        connection = e

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        data = connection.read()
       # print 'got here'
        data = json.loads(data)
    else:
        print 'whoops'
    try:
        week_unformatted = float(json.dumps(data['charts']['chart1']['series'][1]['dataPointsList'][4]['y']))
    except:
        week_unformatted = 0.0

    week = math.floor(week_unformatted*10)/10
    return week

def format_listing(listing):
    ret = ""
    thing = sorted(listing.items() ,key=lambda x: len (x[0] ) )
    for elem in thing :
        ret +=  (elem[0] + " with " +str( elem[1] )+"km\n")
    return ret



for x in range(len(listing.values())):
    listing[listing.keys()[x]] = get_this_week_from_URL(listing.values()[x])

#print listing

highscore_formatted = format_listing(listing)

json_x = {
    'embeds': [
        {
            'title': 'Running-Highscore, this week',
            'footer':{
                'text':'Powered by my nuts'
            },
            'description':'\n'+highscore_formatted
        }
    ]
}

headers = {"content-type": "application/json"}
r = requests.post(webhook,headers=headers,data=str(json.dumps(json_x)))
