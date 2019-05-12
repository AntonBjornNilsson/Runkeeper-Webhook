from bs4 import BeautifulSoup
import urllib2
import json
import math
import requests
import operator
import datetime


webhook="""
YOUR WEBHOOK URL HERE
"""

listing = {
    'Friend1' : "https://runkeeper.com/user/Friend1/fitnessReportsData",
    'Friend2' : "https://runkeeper.com/user/Friend2/fitnessReportsData",
    'Friend3' : "https://runkeeper.com/user/Friend3/fitnessReportsData",
    'Friend4' : "https://runkeeper.com/user/Friend4/fitnessReportsData"
}

dt = datetime.datetime.now()
dt_b4 = (datetime.date.today() - datetime.timedelta(1*365/12))
dt = dt.strftime("%d-%b-%Y")
dt_b4 = dt_b4.strftime("%d-%b-%Y")

params = (
    "startDate="+dt_b4+"&endDate="+dt+"&timeframeOption=LAST_30_DAYS&chartTimeBuckets=WEEK&reportConfigJson=%7B%22totalBoxes%22%3A%7B%22TOTAL_DISTANCE%22%3A%7B%22field%22%3A%22TOTAL_DISTANCE%22%7D%7D%2C%22charts%22%3A%7B%22chart1%22%3A%7B%22field%22%3A%22TOTAL_DISTANCE%22%2C%22stack%22%3A%22true%22%7D%7D%7D"
)

backup = listing.copy()
method = "POST"
handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)



def get_this_week_from_URL(URL):
    data = None
    request = urllib2.Request(URL, params)
    request.get_method = lambda: method
    try:
        connection = opener.open(request)

    except urllib2.HTTPError,e:
        connection = e
    if connection.code == 200:
        data = connection.read()
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
    list_view = [ (v,k) for k,v in listing.iteritems() ]
    list_view.sort(reverse=True)
    winner = backup[list_view[0][1]]
    for v,k in list_view:
        ret+= k + " with **"+str(v)+"**km\n"
    return ret,winner


for x in range(len(listing.values())):
    listing[listing.keys()[x]] = get_this_week_from_URL(listing.values()[x])

highscore_formatted,winner = format_listing(listing)

r = urllib2.urlopen(winner.replace("Data","/cardio")).read()
soup = BeautifulSoup(r,'html.parser')


winner_url = soup.find_all('img')[1]['src']

json_x = {
    'embeds': [
        {
            'title': 'Last Weeks Highscore\nMost km in cardio',
            'footer':{
                'text':'Powered by my nuts'
            },
            "thumbnail": {
                "url": winner_url
            },
            'description':'\nAnd the Winner IS:\n\n '+highscore_formatted
        }
    ]
}

headers = {"content-type": "application/json"}
r = requests.post(webhook,headers=headers,data=str(json.dumps(json_x)))

