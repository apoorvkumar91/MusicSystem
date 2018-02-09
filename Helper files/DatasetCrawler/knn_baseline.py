import pandas as pd
import os
import collections
import operator

def getCleanUserList(inUsers):
    inUsers = inUsers.replace('\"', '')
    inUsers = inUsers.replace('[', '')
    inUsers = inUsers.replace(']', '')
    inUsers = inUsers.replace('\'', '')
    return inUsers.split(', ')

def getCleanScoreList(inScore):
    retVal = []
    inScore = inScore.replace('[', '')
    inScore = inScore.replace(']', '')
    tmpList = inScore.split(', ')
    for i in tmpList:
        retVal.append(float(i))
    return retVal

def getSongCorpus(inUsers):
    base_directory = '/Users/sidverma/Desktop/IR/'
    os.chdir(base_directory)
    df = pd.read_csv('Final.csv')
    groupFrame = df.groupby(by = 'Users')
    corpus = set()
    for usr in inUsers:
        currFrame = groupFrame.get_group(usr)
        songsPool = currFrame.Songs.tolist()
        for s in songsPool:
            corpus.add(s)
    return corpus

def calculateSongsInvertedIndex(inUserList, inCorpus):
    invertedIndexDict = collections.defaultdict(list)
    base_directory = '/Users/sidverma/Desktop/IR/'
    os.chdir(base_directory)
    df = pd.read_csv('Final.csv')
    groupFrame = df.groupby(by='Users')
    for user in inUserList:
        currFrame = groupFrame.get_group(user)
        userSongsList = currFrame.Songs.tolist()
        for s in userSongsList:
            invertedIndexDict[s].append(user)
    return invertedIndexDict

def getSongScore(song, inUser, occuringPlayLists, neighbor_scores_tuples_list):
    retVal = 0.0
    for tup in neighbor_scores_tuples_list:
        neighbor = tup[0]
        neighborScore = tup[1]
        if neighbor in occuringPlayLists:
            retVal += neighborScore
    return retVal

def calculateSimilarityMeasure(inUser, inInvertedScoresDict, neighbor_scores_tuples_list):
    scoresDict = collections.defaultdict(float)
    for song in inInvertedScoresDict:
        score = getSongScore(song, inUser, inInvertedScoresDict[song], neighbor_scores_tuples_list)
        scoresDict[song] = score
    return scoresDict

def knnSimilarity(inUserList):
    base_directory = '/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DatasetCrawler/'
    os.chdir(base_directory)
    df = pd.read_csv('knnSimilarity.csv')
    userFrame = df.groupby(by='Users')
    index = 0
    userAlreadyVisited = set()
    for i, row in df.iterrows():# in userCol[:_SAMPLESIZE]:
        u = row['Users']
        if u not in inUserList:
            continue
        if u in userAlreadyVisited:
            continue
        userAlreadyVisited.add(u)
        neigbors = row['kNN']
        userList = getCleanUserList(neigbors)
        simScores = row['Similarities']
        simScoresList = getCleanScoreList(simScores)
        neighbor_scores_tuples_list = zip(userList, simScoresList)
        print 'Genrating CORPUS'
        currCorpus = getSongCorpus(userList)
        print 'Done CORPUS GENERATION'
        print u, len(currCorpus)
        print '------------'
        print 'Calculating INVERTED INDEX'
        invertedScoresDict = calculateSongsInvertedIndex(userList, currCorpus)
        print 'INVERTED INDEX Calculated'
        print '------------'
        print 'Calculating SCORES ', u
        similarityScores = calculateSimilarityMeasure(u, invertedScoresDict, neighbor_scores_tuples_list)
        print 'SCORES Calculated ', u
        print '------------'
        #t = sorted(similarityScores.items(), key=operator.itemgetter(1), reverse=True)
        final_df = pd.DataFrame(similarityScores.items(), columns=['Songs', 'Score'])
        fname = u + 'KNN_Score.csv'
        print "Taking a dump " + fname
        final_df.to_csv(fname)
        # for tu in t[:199]:
        #     print tu
userList = ['Babs_05']
knnSimilarity(userList)
print 'DONE'