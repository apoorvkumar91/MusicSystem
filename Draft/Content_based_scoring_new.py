#packages and libraries
import pandas as pd
import math
import time
import random
import sys
import os
import collections
import operator
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
frame.drop(["Playtime", "Album", "Match" , "Listeners", "Playcount", "Duration", "Tags"], axis=1, inplace="True")

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


def normalizeByPlaylistLength(tf_idf_vector, playlist_length):
    normalized_vec=[(value/float(playlist_length)) for value in tf_idf_vector]
    return normalized_vec

# calculating the user content based on the history
def claculateContentBasedNewScore(user):
    user_group = groupedUsers.get_group(user)
    print user_group.Songs.tolist()
    Full_list = user_group.TagVector.tolist()
    Train_list = Full_list[0:int(math.ceil(split_ratio*len(Full_list)))]
    list_tag_vectors=[]
    for tag_vector in Train_list:
        track_tag_vector= tag_vector.split('$')
        track_tag_vector_final=[int(value) for value in track_tag_vector]
        list_tag_vectors.append(track_tag_vector_final)
    TF_IDF_vector_list=[]
    for tag_vector in list_tag_vectors:
        TF_IDF_listvec = TF_IDF_generator(tag_vector)
        TF_IDF_vector_list.append(TF_IDF_listvec)

    TF_IDF_history = [sum(x) for x in zip(*TF_IDF_vector_list)]
    UserList_normalized = normalizeByPlaylistLength(TF_IDF_history,len(Train_list))
    UserList_normalized=normalizefunction(UserList_normalized)

    ScoringDict = collections.defaultdict(list)
    i=0
    for song in groupsSongs:
        tags_list = groupedSongs.get_group(song).Tags.tolist()
        songlistString =  str(tags_list[0]).split("$")
        this_track_tag_vector = [int(value) for value in songlistString]
        TF_IDF_thistrack=TF_IDF_generator(this_track_tag_vector)
        TF_IDF_thistrack=normalizefunction(TF_IDF_thistrack)
        scoring_val = cosinefunction(UserList_normalized, TF_IDF_thistrack)
        ScoringDict[song] = scoring_val
        i+=1
    similar_neighbors=[]
    similarity_scores=[]
    reversesorteditems = sorted(ScoringDict.items(), key=operator.itemgetter(1), reverse=True)
    count=0
    for item  in reversesorteditems:
        if count == 1000:
           break
        similar_neighbors.append(str(item[0]))
        similarity_scores.append(str(item[1]))
        count = count + 1
    return similar_neighbors, similarity_scores





def calculate_for_all():
    for user in groupsUsers.keys()[:2]:
        #print "Printing the length of the users"
        print user
        #print "Ending the users"
        user_list.append(user)
        #score_list = Calculate_content_based_score(user)
        songlist, score_list = claculateContentBasedNewScore(user)
        #[neb_list,score_list] =  Calculate_content_based_score(allusers)
        #neighbours_list.append(neb_list)
        zip(songlist, score_list)
        scores_list.append(zip(songlist, score_list))


calculate_for_all()

df = pd.DataFrame(
    #data={"Users": user_list, "Neighbours": neighbours_list, "Similarities": scores_list },
    data={"Users": user_list,"Similarities": scores_list },
    columns=["Users", "Similarities"])
df.to_csv("ContentBasedSimilarity.csv", sep=',')
