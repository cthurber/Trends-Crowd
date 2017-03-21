
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
def toDataFrame(filename,icol=0): return pd.read_csv(filename,index_col=int(icol))
def masterFileExists(feedname,feeddir): True if(feedname in os.listdir(feeddir)) else False

# Returns {feedname : [DataFrame1,DataFrame2, ...]} pairing
def mapDataFrames(cache_path):
    filenames = {}
    for key in getFilenameKeys(cache_path):
        filenames[key] = [toDataFrame(cache_path + str(filename)) for filename in os.listdir(cache_path) if key == getRootFeed(filename)]
    return filenames

df_index = (mapDataFrames(cache_path))
print(df_index)

# for feed in index
if(masterFileExists(feed,output_path)):
    # merge all new dataframes with master from 'data' folder
#   if no: write merged version from df_index

# Write merged version
"""
for df in dfs:
    frame = dfs[df][0]
    frame.to_csv("./data/"+str(df)+".csv")
"""
