
"""

Trends-Crowd Queue Layer
Author: Chris Thurber
Created: March 22, 2017
Descrip: Scheduling daemon responsible for data collection

"""

import time, os
from random import randint
from acquire import saveFeed, nameFile, getURLComps
from merge import mergeFeeds, toDataFrame

def main(schedule,record):
    while(True):

        if not os.path.exists(schedule): os.makedirs(schedule)
        with open(schedule,'r') as s:
            queue = [line.replace('\n','') for line in s]

        if os.path.exists(record):
            with open(record,"r") as r:
                feeds_run = [line.replace('\n','') for line in r]
        else:
            feeds_run = []
            record = open(record,'w')
            record.close()

        if(len(queue) < 0):
            print("Waiting for additional feeds...")
            time.sleep(62)
        else:
            queue = list(set(queue))
            print(queue)
            with open("./feed_runs.csv","a") as work_done:
                for feed in queue:
                    feedname = nameFile(feed,time=False)
                    if feedname not in feeds_run:
                        # BUG: Feedname sometimes shows as None, cannot process even though components return
                        # print(feed)
                        # print(getURLComps(feed))

                        print("Running",feedname)
                        time.sleep(randint(60,70))
                        saveFeed(feed)
                        print(feedname,file=work_done)
            mergeFeeds()

main("./schedule.csv","./feed_runs.csv")
