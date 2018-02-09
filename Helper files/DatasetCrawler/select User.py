import pandas as pd
import os
import collections
import numpy as np
import operator
import matplotlib.pyplot as plt
import random

_PLAYLIST_SIZE_THRESHOLD = 150
_TAGS_THRESHOLD = 25
_GOOD_RATIO = 0.8
base_directory = '/Users/sidverma/Desktop/IR/'
def getUserDataPlot():
    os.chdir(base_directory)
    df = pd.read_csv('Final.csv')
    groupFrame = df.groupby(by = 'Users')
    groupedUsers  = groupFrame.groups
    currrame = df.groupby(by='Users')
    X = xrange(len(groupedUsers))
    Y = []
    goodUsers = []
    for user in groupedUsers.keys():
        currFrame = groupFrame.get_group(user)
        songsPool = currFrame.Songs.tolist()
        Y.append(len(songsPool))
        if len(set(songsPool))>=_PLAYLIST_SIZE_THRESHOLD:
            goodUsers.append(user)
    freq = collections.Counter(Y)
    #for i in freq:
    #    print i, freq[i]
    '''
    #Uncomment to get teh plot
    choices = np.random.choice(len(X), 50)
    X_S = xrange(50)
    Y_S = []
    for c in choices:
        Y_S.append(Y[c])
    plt.bar(X_S, Y_S)
    plt.grid()
    plt.show()
    '''
    return goodUsers

def isGooodTagList(inTagsStr):
    inStrList = inTagsStr.split('$')
    summ = 0
    for i in inStrList:
        if i == '1':
            summ += 1
    if summ<_TAGS_THRESHOLD:
        return False
    else:
        return True

def getGoodSongsPool():
    goodSongSet = set()
    os.chdir(base_directory)
    df = pd.read_csv('FinalTagroomMergedVecs.csv')
    songList = set()
    for i, row in df.iterrows():
        sng = row['Songs']
        if sng in songList:
            continue
        tagStr = row['Tags']
        if isGooodTagList(tagStr):
            songList.add(sng)
    return songList

def isUserGoodEnough(songsPool, goodSongsSet):
    goodSongsOfThisPool = 0
    for sng in songsPool:
        if sng in goodSongsSet:
            goodSongsOfThisPool+=1
    ratio = (1.0*goodSongsOfThisPool) / len(songsPool)
    if ratio >= _GOOD_RATIO:
        return True
    else:
        return False

def getTagetUsers():
    print 'Getting GoodUser Pool'
    goodUsernames = getUserDataPlot()
    print len(goodUsernames)
    print 'Done Getting GoodUser Pool'
    print 'Getting GoodSongs Pool'
    goodSongsSet = getGoodSongsPool()
    print len(goodSongsSet)
    print 'Done Getting GoodSongs Pool'
    retTagetUsers = []
    os.chdir(base_directory)
    df = pd.read_csv('Final.csv')
    groupFrame = df.groupby(by='Users')
    print 'Getting AwesomeUser Pool'
    for user in goodUsernames:
        currFrame = groupFrame.get_group(user)
        songsPool = set(currFrame.Songs.tolist())
        if isUserGoodEnough(songsPool, goodSongsSet):
            retTagetUsers.append(user)
    print 'Done Getting AwesomeUser Pool'
    return retTagetUsers

tmp = getTagetUsers()
print tmp,'\nDone '

file = open('Best_Users.txt', 'w')
for user in tmp:
    file.write(user)
file.close()
print "Wrote to file..."


