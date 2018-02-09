import pandas as pd
import random
import sys
import numpy as np
import collections
import os
import operator
import math

split_ratio_train_test = 0.8
split_ratio_train = 0.2
base_directory = '/Users/sidverma/Desktop/IR/SCORE'
os.chdir(base_directory)
DataSetFile = "Final.csv"
frame = pd.read_csv(DataSetFile)
frame.drop(["Playtime", "Album", "Match"], axis=1, inplace="True")

grouped1 = frame.groupby(by="Songs")
groups1 = grouped1.groups

groupedusers =frame.groupby(by="Users")
groupsusers = groupedusers.groups

groupedartist = frame.groupby(by='Artists')
groupsartist = groupedartist.groups

user_list=[]
song_list=[]
listener_count = []
duration_count = []
artist_list = []
SongsList = []
Artist_scoring_ratio = 0.2

neighbours_list = []
scores_list = []

def artist_scoring_based_score(userlist):
  for username in userlist:
    songdict = {}
    artist_list = []
    user_list=[]
    user_list.append(username)
    user_group=groupedusers.get_group(username)
    Full_list = user_group.Artists.tolist()
    content_start_index = len(Full_list)- int(math.ceil(split_ratio_train_test*len(Full_list)))
    content_end_index  = content_start_index + int((split_ratio_train)* (math.ceil(split_ratio_train_test*len(Full_list))))
    Train_list = Full_list[content_start_index:content_end_index]
    artist_list.extend(Full_list)
    artist_dict = collections.Counter(artist_list)
    similar_neighbors=[]
    similarity_scores=[]
    artist_name = max(artist_dict, key=artist_dict.get)
    if artist_dict[artist_name] > Artist_scoring_ratio * len(artist_list):
       for itr, row in groupedartist.get_group(artist_name).iterrows():
          if math.isnan(row["Playcount"]):
               songdict[row["Songs"]] = 0.0
          else:
               songdict[row["Songs"]] = row["Playcount"]
  
       reversesorteditems = sorted(songdict.items(), key=operator.itemgetter(1), reverse=True)
       count = 0
       
       for  items in reversesorteditems:
          similar_neighbors.append(str(items[0]))
          similarity_scores.append(items[1])
    else:
          similar_neighbors.append("")
          similarity_scores.append("")
    print user_list
    print similar_neighbors
    print similarity_scores
    neighbours_list = []
    scores_list = []
    neighbours_list.append(similar_neighbors)
    scores_list.append(similarity_scores)
    df = pd.DataFrame(data={"Users": user_list, "Neighbours": neighbours_list, "Similarities": scores_list }, 
             columns=["Users", "Neighbours", "Similarities"]) 
    df.to_csv(str(username) + "ARTIST_SCORE.csv", sep=',')
userlist = ['monkeyhacker','badboy495','sonnycorleones','heavydirtysoul_','Garry_Drezden']
artist_scoring_based_score(userlist)




    
    



    
