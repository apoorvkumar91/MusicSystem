#packages and libraries
import pandas as pd
import math
import time
import os

basedir = '/Users/sidverma/Desktop/IR/'
os.chdir(basedir)

def similarity_func(playlist1, playlist2):
    set2 = set(playlist2)
    count=[1 for song in playlist1 if song in set2]
    return float(sum(count))/math.sqrt(len(playlist1)*len(playlist2))
split_ratio=0.8
start=time.time()

frame = pd.read_csv("Final.csv")
frame.drop(["Playtime", "Album", "Match" , "Listeners", "Playcount", "Duration", "Tags"], axis=1, inplace="True")
grouped=frame.groupby(by="Users")
groups=grouped.groups

user_list=[]
song_list=[]
for k in groups.keys():
    user_list.append(k)
    user_group=grouped.get_group(k)
    song_list.append(user_group.Songs.tolist())
similarities=[]

len_user_list=len(user_list)
for i, user in enumerate(user_list):
    print "Calculating 300NN for User", i
    similarity=[]
    end_index=int(math.ceil(split_ratio*len(song_list[i])))
    curr_user_playlist=song_list[i][:end_index]
    print "User details: ", user, len(curr_user_playlist)
    for j in range(0,i):
        print "Parsing Row: ", j
        similarity.append((user_list[j],similarity_func(curr_user_playlist, song_list[j])))
    for j in range(i+1, len_user_list):
        print "Parsing Row: ", j
        similarity.append((user_list[j], similarity_func(curr_user_playlist, song_list[j])))
    similarities.append(similarity)


for i in  range(len(similarities)):
    #similarities[i].sort(key=itemgetter(2), reverse="True")
    similarities[i].sort(key = lambda x: float(x[1]), reverse = True)
    similarities[i]=similarities[i][:300]

similar_neighbors=[]
similarity_scores=[]
for similarity in similarities:
    curr_similar_neighbors=[similar[0] for similar in similarity]
    curr_similarity_score=[similar[1] for similar in similarity]
    similar_neighbors.append(curr_similar_neighbors)
    similarity_scores.append(curr_similarity_score)

df = pd.DataFrame(
    data={"Users": user_list, "kNN": similar_neighbors, "Similarities": similarity_scores },
    columns=["Users", "kNN", "Similarities"])
df.to_csv("knnSimilarity.csv", sep=',')






