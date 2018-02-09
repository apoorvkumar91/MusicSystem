import collections
import pandas as pd
import os
import math

base_directory = 'Project_folder/'
os.chdir(base_directory)
DataSetFile = "Final.csv"

frame = pd.read_csv(DataSetFile)
frame.drop(["Playtime", "Album", "Match" , "Listeners", "Playcount", "Duration"], axis=1, inplace="True")

groupedUsers = frame.groupby(by="Users")
groupsUsers=groupedUsers.groups

groupedSongs = frame.groupby(by="Songs")
groupsSongs=groupedSongs.groups

# Input: 20% of User Playlist and Top - K ranked Songs from Song Corpus
def ComputePlaylistTagAvg(username):
        Full_list_len = len(groupedusers.get_group(username).Songs.tolist())
        end_index = Full_list_len - math.ceil(split_ratio_train_test*Full_list_len)
	Sum_Vector = []
	for index, row in groupedusers.get_group(username).iterrows():
                if index == end_index:
                    break:
		for tag_index, tag_value in enumerate(row['Tags']):
			Sum_Vector[tag_index] += tag_value
	for tag_sum_index, tag_sum_value in Sum_Vector:
		Sum_Vector[tag_sum_index] = tag_sum_value/float(DataFrame.shape[0])
	return Sum_Vector


def ComputeSim(user_avg_tag_veg, ranked_song_tag_vec):
	total = 0.0
	for i in xrange(len(user_avg_tag_veg)):
		total += user_avg_tag_veg[i]*ranked_song_tag_vec[i]
	return total / (float(len(user_avg_tag_veg) * len(ranked_song_tag_vec)) ** 0.5)


def GetIntraSimScore(Similarity_dict, Song_Index):
	total = 0.0
	counter = 0.0
	for key, value in Similarity_dict.iteritems():
		if Song_Index in key[0]:
			total += value
			counter += 1.0
	return total/counter


def Next_track_optimization():
userlist = ['monkeyhacker','badboy495','sonnycorleones','heavydirtysoul_','Garry_Drezden']
Scoring_files_content = "File_scoring_1.csv"
Scoring_files_numerical = "File_scoring_2.csv"
Scoring_files_user_pref =  "File_scrogin_3.csv"

df_1 = pd.read_csv(Scoring_files_content)
df_2 = pd.read_csv(Scoring_files_numerical)
df_3 = pd.read_csv(Scoring_files_user_pref)


# Defining Variables
 for user in userlist:
    user_avg_tag_veg = ComputePlaylistTagAvg(user)
    scoring_dict = {}
    for itr, row in df1.iterrows:
       scoring_dict[row["Neighbours"]] = row["Similarities"]
    for itr, row in df2.iterrows:
       scoring_dict[row["Neighbours"]] += row["Similarities"]
    for itr, row in df3.iterrows:
       scoring_dict[row["Neighbours"]] += row["Similarities"]
    reversesorteditems = sorted(scoring_dict.items(), key=operator.itemgetter(1), reverse=True)
    songs_list=[] 
    tags_list = []
    for itr in reversesorteditems:
        songs_list.append(itr)
        tags_list.append(groupedSongs.get_group(itr).Tags.tolist())
    Ranked_song_df = pd.DataFrame(data={"Songs": songs_list,"Tags": tags_list },
          columns=["Songs", "Tags"])
    Similarity_dict = collections.OrderedDict()
    IntraSimScore_dict = collections.OrderedDict()
    # Getting average tag vector from root user


# Code for Intra-Ranked Song Similarity
    for i1, r1 in Ranked_song_df.iterrows():
	for i2, r2 in Ranked_song_df.iterrows():
		if set(i1, i2) in Similarity_dict.keys() or i1 == i2:
			continue
		Similarity_dict[set(i1, i2)] = ComputeSim(r1['Tags'], r2['Tags'])

# Code for Similar to User Distribution


for index in xrange(Ranked_song_df.shape[0]):
	IntraSimScore_dict[index] = GetIntraSimScore(Ranked_song_df, index)
