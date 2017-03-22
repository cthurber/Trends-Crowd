
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

def getFeedName(filename): return re.findall("(.*)__", filename)[0]
def getFilenames(cache_path): return list(set(map(getFeedName, os.listdir(cache_path))))
def getNumCols(filename): return len(open(filename).readline().split(','))
def toDataFrame(filename,icol=0): return pd.read_csv(filename,index_col=int(icol))

# Returns {feedname : [DataFrame1,DataFrame2, ...]} pairing
def mapDataFrames(cache_path):
    # Further efficiency?: dict.fromkeys([1, 2, 3, 4])
    filenames = {}
    for key in getFilenames(cache_path):
        filenames[key] = [toDataFrame(cache_path + str(filename)) for filename in os.listdir(cache_path) if key == getFeedName(filename)]
    return filenames

df_index = (mapDataFrames(cache_path))
print(df_index)

# for feed in index
if(os.path.exists(output_path + feed)):
    # merge all new dataframes with master from 'data' folder
#   if no: write merged version from df_index

# Write merged version
"""
for df in dfs:
    frame = dfs[df][0]
    frame.to_csv("./data/"+str(df)+".csv")
"""
