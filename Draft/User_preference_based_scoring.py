
import pandas as pd
import math
import time
import random
import sys
import os
import collections
import operator
split_ratio_train_test = 0.8
split_ratio_train = 0.3
user_list = []
neighbours_list = []
scores_list = [] 

base_directory = 'Project_folder/'
os.chdir(base_directory)

DataSetFile = "Final.csv"   #Need to check the name of the file
DataSetSongFile = "FinalTagroomMergedVecs.csv"    # Need to check the name of this file
DataSetTagDictFile = "FinalTagFreq.csv"


# reading the main File
frame = pd.read_csv(DataSetFile)
frame.drop(["Playtime", "Album", "Match" , "Listeners", "Playcount", "Duration", "Tags"], axis=1, inplace="True")

# reading the tags related file:
## Songs Based Scoring
frameSong = pd.read_csv(DataSetSongFile)
frameSong["Songs"] = frame["Songs"]
groupedSongs = frameSong.groupby(by="Songs")
groupsSongs = groupedSongs.groups
full_len = frameSong.shape[0]
### Users based grouping 
groupedUsers = frame.groupby(by="Users")
groupsUsers=groupedUsers.groups


# Using the dict for storing the IDF vector
df_dict = pd.read_csv(DataSetTagDictFile)
IDF_DICT = [math.log10((full_len/df_dict['Frequency'][i])) for i in xrange(df_dict.shape[0])]

def findmagnitude(input):
    return math.sqrt(sum(input[i]*input[i] for i in range(len(input))))

def normalizefunction(input):
    listmagnitude =  findmagnitude(input)
    if  listmagnitude == 0:
        return  input
    return [ float(input[i])/listmagnitude  for i in range(len(input)) ]

def cosinefunction(input1, input2):
    return sum(input1[i]*input2[i] for i in range(len(input1)))

def TF_IDF_generator(input):
    return_list = []
    for i in xrange(len(input)):
        if input[i]==0:
            val = IDF_DICT[i]
        else:
            val = math.log10(input[i]+1)* IDF_DICT[i]
        return_list.append(val)
    return return_list


# calculating the user content based on the history
def User_preference_based_score(username):
    historyList = []
    historyFullList = []
    user_group = groupedUsers.get_group(username)
    #print user_group.Songs
    Full_list_complete = user_group.Songs.tolist()
    content_start_index = len(Full_list_complete)- int(math.ceil(split_ratio_train_test*len(Full_list_complete)))
    Full_train_list = Full_list_complete[content_start_index:]
    content_end_index  = content_start_index + int((split_ratio_train)* (math.ceil(split_ratio_train_test*len(Full_list_complete))))
    Train_list = Full_list[content_start_index:content_end_index]
    #print Train_list
    for tracks in Train_list:
        tags_len = len(groupedSongs.get_group(tracks).Tags)
        tags_list = groupedSongs.get_group(tracks).Tags.tolist()
        historyListString =  str(tags_list[0]).split("$")
        historytempvec = []
        for itr in historyListString:
            historytempvec.append(int(itr))
        historyList.append (historytempvec)
    TF_listvec = [sum(x) for x in zip(*historyList)]
    for tracks in Full_train_list:
        tags_len = len(groupedSongs.get_group(tracks).Tags)
        tags_list = groupedSongs.get_group(tracks).Tags.tolist()
        historyListFullString =  str(tags_list[0]).split("$")
        historyFulltempvec = []
        for itr in historyFullListString:
            historyFulltempvec.append(int(itr))
        historyFullList.append (historyFulltempvec)  
    TF_listFullvec = [sum(x) for x in zip(*historyFullList)]
    TF_IDF_listvec = TF_IDF_generator(TF_listvec)
    TF_IDF_Fulllistvec = TF_IDF_generator(TF_listFullvec)
    UserList_normalized = normalizefunction(TF_IDF_listvec)
    UserFullList_normalized = normalizefunction(TF_IDF_Fulllistvec)
    ScoringDict = collections.defaultdict(list)
    for allusers in groupsUsers.keys():
        print allusers
        if allusers == username:
            continue
        for tracks in groupedUsers.get_group(allusers).Songs.tolist():
             if tracks in ScoringDict:
                 continue
             songtempvec = []
             tags_list = groupedSongs.get_group(tracks).Tags.tolist()
             songlistString =  str(tags_list[0]).split("$")
             for  index,itr in enumerate(songlistString):
                  songtempvec.append(int(itr))
             TF_IDF_songvec = TF_IDF_generator(songtempvec)
             song_normalized = normalizefunction(TF_IDF_songvec)
             ScoringDict[tracks]= Preference_factor * cosinefunction(UserList_normalized, song_normalized)+ (1- Preference_factor)* cosinefunction(UserFullList_normalized, song_normalized)
    
    reversesorteditems = sorted(ScoringDict.items(), key=operator.itemgetter(1), reverse=True)
    count = 0
    similar_neighbors=[]
    similarity_scores=[]
    for  items in reversesorteditems:
       if count == 300:
           break
       similar_neighbors.append(str(items[0]))
       similarity_scores.append(str(items[1]))                         
       count = count + 1      
    return similar_neighbors, similarity_scores

def calculate_for_all():
    user_list = []
    neigbours_list = []
    scores_list = []                        
    for allusers in groupsUsers.keys()[0:10]:
        user_list.append(allusers)
        neb_list, score_list =  User_preference_based_score(allusers)                    
        neigbours_list.append(neb_list)
        scores_list.append(score_list)

df = pd.DataFrame(
    data={"Users": user_list, "Neighbours": neighbours_list, "Similarities": scores_list },
    columns=["Users", "Neighbours", "Similarities"])
df.to_csv("ContentBasedSimilarity.csv", sep=',')

    
