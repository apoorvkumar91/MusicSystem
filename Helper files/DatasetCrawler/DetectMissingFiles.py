### Code Block to Detect Missing Playlists
import os
_BASE_DIRECTORY_ = []
idx = 0
for k in [0, 1, 3, 4, 5]:
	_BASE_DIRECTORY_.append('/Users/sidverma/Documents/GitHub/CS670MyTunes/Helper files/DataSetCrawler_niksy/UserPlaylist' + str(k+1) + '/')
	dirs = os.listdir(_BASE_DIRECTORY_[idx])
	idx += 1
	#print dirs
	tmp = []
	for f in sorted(dirs):
		if f[8:-4] == '':
			continue
		tmp.append(f[8:-4])
		#tmp += f[8:-4],
	tmp = sorted(tmp, key = int)
	print "For dir" + str(k+1) + ":"
	for i in xrange(0, len(tmp)-1):
		if int(tmp[i]) != int(tmp[i+1])-1:
			print i+1



 	