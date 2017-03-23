
"""

Trends-Crowd Merge Layer
Author: Chris Thurber
Created: March 21, 2017
Descrip: Handles merge and move of files from cache into data folder for delivery

"""

import os,re
import pandas as pd

def getFeedName(filename): return re.findall("(.*)__", filename)[0]
def getFilenames(cache_path): return list(set(map(getFeedName, os.listdir(cache_path))))
def getNumCols(filename): return len(open(filename).readline().split(','))
def toDataFrame(filename,icol=0): return pd.read_csv(filename,index_col=int(icol))

# Returns {feedname : [DataFrame1,DataFrame2, ...]} pairing
def mapDataFrames(cache_path):
    filenames = {}
    for key in getFilenames(cache_path):
        filenames[key] = [toDataFrame(cache_path + str(filename)) for filename in os.listdir(cache_path) if key == getFeedName(filename)]
    return filenames

def mergeFeeds(cache_path="./cache/csv/", output_path="./data/"):

    index = mapDataFrames(cache_path)

    for feed in index:
        if not os.path.exists(output_path): os.makedirs(output_path)
        if(os.path.exists(output_path + feed)):
            index[feed].append(toDataFrame(output_path + feed + ".csv"))

        df = pd.concat(index[feed])
        df = df.drop_duplicates(subset='Date')
        # Make caching so as to not lose data on bad write
        df.to_csv(output_path + feed + ".csv")
        # Clear cache
