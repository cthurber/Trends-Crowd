
"""

Trends-Crowd Acuisition Layer
Author: Chris Thurber
Created: February 24, 2017
Descrip: Responsible for parsing user-friendly Trends URLs to JSON counterparts + downloading data

"""

import json,requests,re,os
import pandas as pd
from time import gmtime, strftime

def getURLComps(page_url):
    page_url = str(page_url)
    components = {
        "date" : re.findall("date=([a-z]+%[0-9]+-.)",page_url)[0] if "date=" in page_url else "None",
        "frequency" : re.findall("date=([a-z]+%[0-9]+-.)",page_url)[0].split('%20')[1] if "date=" in page_url else "2004-p",
        "queries" : re.findall("q=(.*)",page_url)[0].replace(' ','%20').split(',') if "q=" in page_url else ["None"],
        "geo" : re.findall("geo=([A-Z]+)",page_url)[0] if "geo=" in page_url else "Worldwide"
        "cat" : re.findall("cat=([0-9]+)", page_url)[0] if "cat=" in page_url else "All"
    }

    return components

def parseURL(page_url):

    comps = {
        "base" : "http://www.google.com/trends/fetchComponent?hl=en-US",
        "export" : "&export=3",
        "content" : "&content=1",
        "cid" : "&cid=TIMESERIES_GRAPH_0",
        "date" : "&date=",
        "query" : "&q=",
        "time" : "&tz=Etc/GMT%2B4"
    }

    if("fetchComponent" in page_url): return page_url

    # TODO Edit page to make possible to enter terms
    if("http" not in page_url):
        return comps['base'] + comps['date'] + "today%203-m" + comps['query'] + page_url.replace(' ','%20') + comps['time'] + comps['content'] + comps['cid'] + comps['export']

    filters = getURLComps(page_url)

    query_string = str(filters['queries']).replace("'",'').replace('[','').replace(']','').replace(', ',',')
    feed_url = comps['base'] + comps['date'] + filters['date'] + comps['query'] + query_string + comps['time'] + comps['content'] + comps['cid'] + comps['export']

    return feed_url

def cleanFeed(json_feed):
    clean_feed = json_feed.replace('}{','},{').replace(",,",',').replace('new Date','').replace("(", "[").replace(")", "]").replace('} {','}, {').rstrip('];')
    clean_feed = clean_feed.split('setResponse[')[1]

    return clean_feed

def saveJSON(json_feed, cache_dir="cache/json/"):
    if not os.path.exists(cache_dir): os.makedirs(cache_dir)

    with open(cache_dir + nameFile(json_feed) + ".json",'w') as output:
        filename = cache_dir + nameFile(json_feed)+'.csv'
        print(json_feed,file=output)

    return True

def getFeed(page_url):
    feed_url = parseURL(page_url)
    response = requests.get(feed_url)
    json_feed = json.loads(cleanFeed(response.text))

    saveJSON(json_feed)

    return json_feed

def getFeed_Test(file_url):
    fstring = ""
    with open(file_url, 'r') as testfile:
        for line in testfile:
            fstring += line

    json_feed = json.loads(cleanFeed(fstring))

    saveJSON()

    return json_feed

def translateCSV(json_feed):

    # Create 2D array
    cols = json_feed['table']['cols']
    headers = [col['label'] for col in cols]
    rows = json_feed['table']['rows']

    data_frame = []
    for row in rows:
        isNull = False
        nrow = [row['c'][0]['f']]
        for col in row["c"][1:]:
            if(str(col['v']) == 'None'): isNull = True
            nrow.append(col['v'])
        if(isNull == False):
            data_frame.append(nrow)

    data_frame = pd.DataFrame(data_frame, columns=list(headers))
    return data_frame

def nameFile(page_url,date=True,time=True,csv=False):

    if("http:" not in page_url): return page_url

    name = ""
    comps = getURLComps(page_url)

    for q in comps['queries']:
        name += q + ' '

    name += comps['frequency'] + '_'

    if(date): name += strftime("_%Y-%m-%d", gmtime())
    if(time): name += strftime("_%H:%M:%S", gmtime())
    if(csv): name += '.csv'

    return name.replace(' ','_')

def saveFeed(page_url, cache_dir="cache/csv/"):
    cache_dir = cache_dir if '/' in cache_dir else cache_dir + '/'
    feed = getFeed(page_url)

    df = translateCSV(feed)
    filename = cache_dir+nameFile(page_url)+'.csv'
    if not os.path.exists(cache_dir): os.makedirs(cache_dir)

    df.to_csv(filename)

    return True
