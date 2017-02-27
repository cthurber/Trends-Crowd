
"""

Trends-Crowd Acuisition Layer
Author: Chris Thurber
Created: February 24, 2017
Descrip: Responsible for parsing user-friendly Trends URLs to JSON counterparts + calling C++ scraper

"""

import json,requests,re
import pandas as pd
from time import gmtime, strftime

def parseURL(page_url):
    filters = {
        "date" : re.findall("&date=(.*\d+\-.)&.",page_url)[0],
        "query" : re.findall("&q=(.*)",page_url)[0].replace(' ','%20'),
        "geo" : re.findall("&geo=(.*)&.",page_url)[0]
    }

    comps = {
        "base" : "http://www.google.com/trends/fetchComponent?hl=en-US",
        "export" : "&export=3",
        "content" : "&content=1",
        "cid" : "&cid=TIMESERIES_GRAPH_0",
        "date" : "&date=",
        "query" : "&q=",
        "time" : "&tz=Etc/GMT%2B4"
    }

    feed_url = comps['base'] + comps['date'] + filters['date'] + comps['query'] + filters['query'] + comps['time'] + comps['content'] + comps['cid'] + comps['export']
    return feed_url

def cleanFeed(json_feed):
    start_string = "// Data table response\n\rgoogle.visualization.Query.setResponse["

    return json_feed.replace('}{','},{').split('setResponse[')[1].replace(",,",',').replace('new Date','').replace("(", "[").replace(")", "]").replace('} {','}, {').rstrip('];')

def getFeed(page_url):
    feed_url = parseURL(page_url)
    response = requests.get(feed_url)
    json_feed = json.loads(cleanFeed(response.text))

    return json_feed

def getFeed_Test(file_url):
    fstring = ""
    with open(file_url, 'r') as testfile:
        for line in testfile:
            fstring += line

    json_feed = json.loads(cleanFeed(fstring))

    return json_feed

def translateCSV(json_feed):

    # Create 2D array
    cols = json_feed['table']['cols']
    headers = [col['label'] for col in cols]
    rows = json_feed['table']['rows']

    data_frame = []
    for row in rows:
        nrow = [row['c'][0]['f']]
        for col in row["c"][1:]:
            nrow.append(col['v'])
        data_frame.append(nrow)

    data_frame = pd.DataFrame(data_frame, columns=list(headers))
    return data_frame

def nameFile(json_feed):

    name = ""

    cols = json_feed['table']['cols']
    headers = [col['label'] for col in cols[1:]]

    for h in headers:
        name += h + "_"

    name += strftime("_%Y-%m-%d_%H:%M:%S", gmtime())

    return name

def writeFeed(page_url, cache_dir="cache/"):
    cache_dir = cache_dir if '/' in cache_dir else cache_dir + '/'
    feed = getFeed(page_url)
    df = translateCSV(feed)
    filename = cache_dir+nameFile(feed)+'.csv'
    df.to_csv(filename)

    return True
