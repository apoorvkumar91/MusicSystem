### Code Block to Check Incomplete Playlists
import os
import pandas as pd
_BASE_DIRECTORY_ = []
idx = 0
for k in [0, 1, 3, 4, 5]:
	_BASE_DIRECTORY_.append('/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler_niksy/UserPlaylist' + str(k+1) + '/')
	dirs = os.listdir(_BASE_DIRECTORY_[idx])
	#print dirs
	for file in dirs:
		if 'playlist' in file:
			temp_df = pd.read_csv(_BASE_DIRECTORY_[idx]+file)
			if temp_df.shape[0] < 1000:
				print file
	idx += 1
	dirs = []