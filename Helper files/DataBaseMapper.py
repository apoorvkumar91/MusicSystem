import numpy as np
import pandas as pd
import os
count = 0
user_pl_dir = '/Users/sidverma/Documents/GitHub/CS670MyTunes/Datasets/Lastfm/Users_6000/'
user_files = os.listdir(user_pl_dir)
#User_DF = pd.read_csv('/Users/sidverma/Documents/GitHub/CS670MyTunes/Datasets/Lastfm/Users_6000/users_playlist_new_0_1500.csv')
User_DF = pd.read_csv('/Users/sidverma/Documents/GitHub/CS670MyTunes/Datasets/Lastfm/Users_6000/users_playlist_new_1500_3000.csv')
count += User_DF.shape[0]
for doc in user_files[2:3]:
	print "Parsing User Document: ", doc
	if 'playlist' in doc:
		#if doc == 'users_playlist_new_0_1500.csv':
		if doc == 'users_playlist_new_1500_3000.csv':
			continue
		temp_df = pd.read_csv(user_pl_dir + doc)
		count += temp_df.shape[0]
		User_DF = pd.concat([User_DF, temp_df], axis = 0)
print User_DF.shape
metadata_base_dir = '/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler/'
metadata_files = os.listdir(metadata_base_dir)

#MetaData_DF = pd.read_csv('/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler/UserPlaylist1/playlist0.csv')
MetaData_DF = pd.read_csv('/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler/UserPlaylist4/playlist0.csv')
index = 0
for folder in metadata_files:
	if 'UserPlaylist' in folder:
		###
		if folder == 'UserPlaylist1' or folder == 'UserPlaylist2' or folder == 'UserPlaylist3':
			continue
		###
		print folder
		playlist_files = os.listdir(metadata_base_dir + folder)
		print len(playlist_files)
		for key in xrange(index*100, len(playlist_files)+index*100):
			print 'Parsing: Playlist', key 
			doc = 'playlist'+ str(key) + '.csv'
			if 'playlist' in doc:
				#if doc == 'playlist0.csv' or doc == 'playlist293.csv':
				if doc == 'playlist0.csv':
					continue
				#print metadata_base_dir + folder + '/' + doc
				temp_df = pd.read_csv(metadata_base_dir + folder + '/' + doc)
				#count += temp_df.shape[0]
				if temp_df.shape[0] < 1000 and doc != 'playlist292.csv':
					#count += 1000 - temp_df.shape[0]
					df_empty = pd.DataFrame(np.nan, index=range(0, 1000 - temp_df.shape[0]), columns=['Songs', 'Listeners', 'Playcount', 'Duration', 'Tags'])
					temp_df = pd.concat([temp_df, df_empty], axis = 0)
					if temp_df.shape[0] == 1000:
						print "################################################################################################################################"
				MetaData_DF = pd.concat([MetaData_DF, temp_df], axis = 0)
		index += 1
#User_DF = User_DF.truncate(after = 200, axis = 0)
#MetaData_DF = MetaData_DF.truncate(after = 200, axis = 0)
User_DF = User_DF.drop('Unnamed: 0', axis = 1)
MetaData_DF = MetaData_DF.drop('Unnamed: 0', axis = 1)
print "Shapes:", User_DF.shape, MetaData_DF.shape
User_DF['Match'] = User_DF['Songs'].isin(MetaData_DF['Songs']).astype(int)

# if 0 in set(User_DF['Match']):
# 	print "DataFrame Mismatch! Exiting Code!"
# 	exit()

print "Successfully Completed Process!"
User_DF['Listeners'] = np.array(MetaData_DF[['Listeners']])
User_DF['Playcount'] = np.array(MetaData_DF[['Playcount']])
User_DF['Duration'] = np.array(MetaData_DF[['Duration']])
User_DF['Tags'] = np.array(MetaData_DF[['Tags']])
print User_DF.shape
print "Count: ", count
print "Number of True Matches: ", len(User_DF.loc[User_DF.Match == 1])
print "Number of False Matches: ", User_DF.shape[0] - len(User_DF.loc[User_DF.Match == 1])

User_DF.to_csv('/Users/sidverma/Desktop/FinalPlaylist.csv')
print "Dumped CSV File"
