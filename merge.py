
"""

Trends-Crowd Merge Layer
Author: Chris Thurber
Created: March 21, 2017
Descrip: Handles merge and move of files from cache into data folder for delivery

"""

import os,re
import pandas as pd

# REMOVE FOR FINAL COPY, REQUIRE CMD ARGS
cache_path = "./cache/"
output_path = "./data/"

def getRootFeed(filename): return re.findall("(.*)__", filename)[0]
def getFilenameKeys(cache_path): return list(set(map(getRootFeed, os.listdir(cache_path))))
def getNumCols(filename): return len(open(filename).readline().split(','))
def toDataFrame(filename): return pd.read_csv(filename,index_col=0)

# Returns {feedname : [DataFrame1,DataFrame2, ...]} pairing
def mapDataFrames(cache_path):
    filenames = {}
    for key in getFilenameKeys(cache_path):
        filenames[key] = []
        for filename in os.listdir(cache_path):
            if key == getRootFeed(filename):
                filenames[key].append(toDataFrame(cache_path + str(filename)))
    return filenames

df_index = (mapDataFrames(cache_path))


# Print at end
"""
for df in dfs:
    frame = dfs[df][0]
    frame.to_csv("./data/"+str(df)+".csv")
"""
