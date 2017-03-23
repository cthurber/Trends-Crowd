
"""

Trends-Crowd Queue Layer
Author: Chris Thurber
Created: March 22, 2017
Descrip: Scheduling daemon responsible for data collection

"""

import time
from random import randint
from acquire import saveFeed
from merge import mergeFeeds

while(True):
    with open("./schedule.csv",'r') as schedule:
        queue = [line.replace('\n','') for line in schedule]
    if(len(queue) < 0):
        time.sleep(62)
    else:
        queue = list(set(queue))
        # TODO Check history to be sure we haven't run this feed today...
        for feed in queue:
            time.sleep(randint(60,70))
            saveFeed(feed)
        mergeFeeds()
