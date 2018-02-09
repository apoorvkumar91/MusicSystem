import pandas as pd
import math
import os
import numpy as np
split_ratio = 0.8
user_list = []
neighbours_list = []
scores_list = []

base_directory = '../data'
os.chdir(base_directory)

DataSetFile = "UserPlaylists.csv"   #Need to check the name of the file
DataSetSongFile = "FinalTagroomMergedVecs.csv"    # Need to check the name of this file
DataSetTagDictFile = "TagFreq.csv"


# reading the main File
frame = pd.read_csv(DataSetFile)
frame.drop(["Playtime", "Album", "Match" , "Playcount", "Duration", "Tags"], axis=1, inplace="True")

# reading the tags related file:
## Songs Based Scoring
frameSong = pd.read_csv(DataSetSongFile)
frame['TagVector']= frameSong['Tags']
frameSong["Songs"] = frame["Songs"]
groupedSongs = frameSong.groupby(by="Songs")
groupsSongs = groupedSongs.groups
full_len = frameSong.shape[0]
### Users based grouping
groupedUsers = frame.groupby(by="Users")
groupsUsers=groupedUsers.groups

groupedMainSongs=frame.groupby(by='Songs')
groupsOfMainSongs=groupedMainSongs.groups

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
    for i in range(len(input)):
        if input[i]==0:
            #val = IDF_DICT[i]
            val=0
        else:
            val = (math.log10(input[i])+1)* IDF_DICT[i]
        return_list.append(val)
    return return_list


def getHit(hiddensong, predictedPlaylist):
    if hiddensong in predictedPlaylist:
        return 1
    else:
        return 0

def getMRR(hiddensong, predictedPlaylist):
    if hiddensong in predictedPlaylist:
        return 1/float((predictedPlaylist.index(hiddensong)+1))
    else:
        return 0


def TagBasedInverseILS(predictedPlaylist):
    TF_IDF_list=[]
    for track in predictedPlaylist:
        tags_list = groupedSongs.get_group(track).Tags.tolist()
        songlistString =  str(tags_list[0]).split("$")
        this_track_tag_vector = [int(value) for value in songlistString]
        TF_IDF_thistrack=TF_IDF_generator(this_track_tag_vector)
        TF_IDF_thistrack=normalizefunction(TF_IDF_thistrack)
        TF_IDF_list.append(TF_IDF_thistrack)
    similarity=0
    for i in range(len(TF_IDF_list)-1):
        for j in range(i+1, len(TF_IDF_list)):
            similarity+= cosinefunction(TF_IDF_list[i], TF_IDF_list[j])
    return 1/similarity


def TagOverLap(userPlayList, predictedPlaylist):
    set_user_list=set()
    set_predicted_list=set()
    for track in userPlayList:
        tags_list = groupedSongs.get_group(track).Tags.tolist()
        set_user_list.update(tags_list)
    for track in predictedPlaylist:
        tags_list = groupedSongs.get_group(track).Tags.tolist()
        set_predicted_list.update(tags_list)
    return float(set_user_list.intersection(set_predicted_list))/ set_user_list.union(set_predicted_list)


def ArtistOverLap(userPlayList, predictedPlaylist):
    set_user_list=set()
    set_predicted_list=set()
    for track in userPlayList:
        artist= groupedMainSongs.get_group(track).Artist.tolist()
        set_user_list.add(artist)
    for track in predictedPlaylist:
        artist= groupedMainSongs.get_group(track).Artist.tolist()
        set_predicted_list.add(artist)
    return float(set_user_list.intersection(set_predicted_list))/ set_user_list.union(set_predicted_list)


def NumericalFeatureMeanAndSTDDifference(userPlayList, predictedPlaylist):
    user_mean = 0
    user_std_dev=0
    pred_mean = 0
    pred_std_dev = 0
    user_listenercount_list=np.array()
    predplaylist_listenercount_list=np.array()
    for track in userPlayList:
        listenercount = groupedSongs.get_group(track).Listeners.tolist()
        user_listenercount_list.appendd(int(listenercount[0]))

    for track in predictedPlaylist:
        listenercount = groupedSongs.get_group(track).Listeners.tolist()
        predplaylist_listenercount_list.appendd(int(listenercount[0]))

    return np.mean(user_listenercount_list)- np.mean(predplaylist_listenercount_list), np.std(user_listenercount_list)- np.std(predplaylist_listenercount_list)




