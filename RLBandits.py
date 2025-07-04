import math
import random
import time
values=[]
counts=[]
nArms=0
def bandit(testNum, armIdx, pullVal):
    time1=time.time()
    global avgValues
    global counts
    global nArms
    if testNum==0:
        counts=[0]*armIdx
        avgValues=[0]*armIdx
        nArms=armIdx
    if testNum>0:

        
        avgValues[armIdx]=((counts[armIdx]*avgValues[armIdx])+pullVal)/(counts[armIdx]+1)

        counts[armIdx]+=1
    for arm in range(nArms):
        if counts[arm]==0:
            return arm

    ucbValues=[0.00]* nArms
    for arm in range(nArms):
        hoffdingValue=(((math.log(testNum))/float(counts[arm])))**0.5
        ucbValues[arm]=avgValues[arm]+(hoffdingValue)
    time2=time.time()
    # print(time2-time1)

    return ucbValues.index(max(ucbValues))
        

#Ashwin Pulla 6 2024


