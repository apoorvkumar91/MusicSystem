import pandas as pd
import collections
import os
from nltk.stem import PorterStemmer
import operator
import matplotlib.pyplot as plt
import threading
import copy

def freq():
    base_directory = '/Users/sidverma/Desktop/IR/'
    os.chdir(base_directory)
    tags_list=[]
    df = pd.read_csv('FinalTagroomMergedVecs.csv')
    tags_list = df['Tags']
    index = 0
    freqDict = {}
    for k in xrange(1000):
        freqDict[k] = 0
    for i in tags_list:
        iList = i.split('$')
        print len(iList)
        if index%500 == 0:
            print index
        for j in xrange(len(iList)):
            if iList[j] == '1':
                freqDict[j] += 1
        index +=1

    tags, freq = [], []
    for i in freqDict:
        tags.append(i)
        freq.append(freqDict[i])

    dfNew = pd.DataFrame(
           data={"Tags": tags, 'Frequency': freq,
                 },columns=["Tags","Frequency"])
    dfNew.to_csv("FinalTagFreq.csv")
    return

freq()
print 'done'