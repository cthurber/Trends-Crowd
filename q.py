
"""

Trends-Crowd Queue Layer
Author: Chris Thurber
Created: March 22, 2017
Descrip: Scheduling daemon responsible for data collection

"""

import time, os
from random import randint
from acquire import saveFeed, nameFile
from merge import mergeFeeds, toDataFrame

def main(schedule,record):
    while(True):

        if not os.path.exists(schedule): os.makedirs(schedule)
        with open(schedule,'r') as s:
            queue = [line.replace('\n','') for line in s]

        if not os.path.exists(record): os.makedirs(record)
        with open(record,"r") as r:
            feeds_run = [line.replace('\n','') for line in r]

        if(len(queue) < 0):
            print("Waiting for additional feeds...")
            time.sleep(62)
        else:
            queue = list(set(queue))

            with open("./feed_runs.csv","a") as work_done:
                for feed in queue:
                    feedname = nameFile(feed,time=False)
                    if feedname not in feeds_run:
                        print("Running",feedname)
                        time.sleep(randint(60,70))
                        saveFeed(feed)
                        print(feedname,file=work_done)
                    else:
                        print("Waiting for additional feeds...")
                        time.sleep(62)
            mergeFeeds()

main("./schedule.csv","./feed_runs.csv")
