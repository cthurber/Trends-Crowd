
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


index = mapDataFrames(cache_path)

for feed in index:
    if not os.path.exists(output_path): os.makedirs(output_path)
    if(os.path.exists(output_path + feed)):
        index[feed].append(toDataFrame(output_path + feed + ".csv"))
    df.concat(index[feed])
    df.drop_duplicates() # This should leave only unique values
    # Set index[feed] = single dataframe from [dataframes]
    # Make caching so as to not lose data on bad write
    df.to_csv(output_path + feed + ".csv")
    # Clear cache
