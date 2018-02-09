import collections
import pandas as pd
import os
import math
# Input: 20% of User Playlist and Top - K ranked Songs from Song Corpus

def ComputePlaylistTagAvg(DataFrame):
	Sum_Vector = []
	for index, row in DataFrame.iterrows():
		for tag_index, tag_value in enumerate(row['Tags']):
			Sum_Vector[i] += tag_value
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

# Defining Variables
User_df = pd.read_csv()
Ranked_song_df = pd.read_csv()
Similarity_dict = collections.OrderedDict()
IntraSimScore_dict = collections.OrderedDict()
# Getting average tag vector from root user
user_avg_tag_veg = ComputePlaylistTagAvg(User_df)

# Code for Intra-Ranked Song Similarity
for i1, r1 in Ranked_song_df.iterrows():
	for i2, r2 in Ranked_song_df.iterrows():
		if set(i1, i2) in Similarity_dict.keys() or i1 == i2:
			continue
		Similarity_dict[set(i1, i2)] = ComputeSim(r1['Tags'], r2['Tags'])

# Code for Similar to User Distribution


for index in xrange(Ranked_song_df.shape[0]):
	IntraSimScore_dict[index] = GetIntraSimScore(Ranked_song_df, index)



