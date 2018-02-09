import pandas as pd
import random
import sys
import numpy as np
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

def calculate_numerical_val(num_feature, mean, variance):
    return (1/math.sqrt(2*math.pi* variance))* math.exp(-1*(math.pow((num_feature-mean),2))/(2* variance))



def numerical_feature_based_score(userlist):
  for username in userlist:
    user_list = []
    user_list.append(username)
    historyList = []
    user_group = groupedusers.get_group(username)
    #print user_group.Songs
    Full_list = user_group.Songs.tolist()
    content_start_index = len(Full_list)- int(math.ceil(split_ratio_train_test*len(Full_list)))
    content_end_index  = content_start_index + int((split_ratio_train)*(math.ceil(split_ratio_train_test*len(Full_list))))
    Train_list = Full_list[content_start_index:content_end_index]
    numlist = []
    songdict = {}
    for itr, row in groupedusers.get_group(username).iterrows():
        numlist.append(row["Playcount"])
    mean_num = np.mean(numlist)
    var_num = np.cov(numlist)   
    for allusers in groupsusers.keys():
        if allusers == username:
            continue
        for itr1,row1 in groupedusers.get_group(allusers).iterrows():
           songdict[row1["Songs"]] = calculate_numerical_val(row1["Playcount"],mean_num,var_num)
    reversesorteditems = sorted(songdict.items(), key=operator.itemgetter(1), reverse=True)
    count = 0
    similar_neighbors=[]
    similarity_scores=[]
    for  items in reversesorteditems:
        similar_neighbors.append(str(items[0]))
        similarity_scores.append(str(items[1]))                       
        count = count + 1
        print user_list
    print similar_neighbors
    print similarity_scores
    scores_list = []
    neighbours_list = []
    neighbours_list.append(similar_neighbors)
    scores_list.append(similarity_scores)
    print neighbours_list
    print scores_list
    df = pd.DataFrame(data={"Users": user_list, "Neighbours": neighbours_list, "Similarities": scores_list }, 
             columns=["Users", "Neighbours", "Similarities"])  
    df.to_csv(str(username) + "NUMERICAL_FEATURES.csv", sep=',')
userlist = ['monkeyhacker','badboy495','sonnycorleones','heavydirtysoul_','Garry_Drezden']

numerical_feature_based_score(userlist)

