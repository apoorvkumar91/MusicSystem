import pandas as pd
import random
import sys
import numpy as np
DataSetFile = "FinalData1/Final.csv"
#DataSetFile = "FinalData/Final_Playlist_Users_test_0_1500.csv"
frame = pd.read_csv(DataSetFile)
frame.drop(["Playtime", "Album", "Match"  ], axis=1, inplace="True")
grouped1 = frame.groupby(by="Songs")
groups1 = grouped1.groups
grouped=frame.groupby(by="Users")
groups=grouped.groups
groupedartist = frame.groupby(by='Artists')
groupsartist = groupedartist.groups


PersonalizedScoringvalue = 0.2
user_list=[]
song_list=[]
listener_count = []
duration_count = []
artist_list = []
SongsList = []
for k in groups.keys():
    user_list.append(k)
    user_group=grouped.get_group(k)
    song_list.append(user_group.Songs.tolist())
artist_list.append(grouped.get_group("Babs_05").Artists.tolist())
print artist_list
artist_set = set(artist_list[0])
if len(artist_set) ==1:
    SongsList.append(groupedartist.get_group(list(artist_set)[0]).Songs.tolist())

print SongsList




user_listener_count = np.mean(np.array(listener_count))
user_duration_count = np.mean(np.array(duration_count))
print user_listener_count
print user_duration_count
#print grouped.get_group("Babs_05")
print user_list.append(grouped1.get_group("Spoonful").Tags.tolist())
print user_list
print song_list


def findmagnitude(input):
    return math.sqrt(sum(input[i]*input[i] for i in range(len(input))))

def normalizefunction(input):
    listmagnitude =  findmagnitude(input)
    if  listmagnitude == 0:
        return  input
    return [ float(input[i])/listmagnitude  for i in range(len(input)) ]

def cosinefunction(input1, input2):
    return sum(input1[i]*input2[i] for i in range(len(input1)))

username = "Babs_05"
collectivehistorylist  = []
historyvec = []
collectivehistoryvec
historylist = []
for tracks in grouped.get_group(username).Songs.tolist():
    print tracks
    collectivehistorylist.append (grouped1.get_group(tracks).Listeners.tolist())
print (zip(*collectivehistorylist))
#historylist = [[6323], [4348], [1913], [1539], [3479]]
listsum = [sum(x) for x in zip(*historylist)]
print listsum
print historylist


songsdict = collections.defaultdict(list)

for username in nearestneighbourlist:
    for track in username:
        songslist = df[start_column:end_column]
        songsdict[track]= PersonalizedScoringvalue * cosinefunction(historyvector,songlist) + (1- PersonalizedScoringvalue)* cosinefunction(collectivehistoryvector,songlist)

        
reversesorteditems = sorted(songsdict.items(), key=operator.itemgetter(1), reverse=True)
count = 0
for  items in reversesorteditems:
    if count == 50:
        break
    print (str(items[0]) + "--" + str(items[1]))
    count = count + 1      


    
    



    
