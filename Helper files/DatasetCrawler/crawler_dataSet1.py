import pylast
import pandas as pd
import re
import json

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account/create for Last.fm
API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
count1=200
output_file_location= "Crawlers/users.csv"

def getFriends(friend):
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                   username=friend, password_hash=None)
    user = pylast.User(friend, network)
    friends = user.get_friends(10, True)
    return friends


def networkdeclaration(username):
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                   username=username, password_hash=None)
    return network


def BFS(username,count,friendlist):
    queue = []
    queue.append(username)
    i=0
    while queue and i<count:
        # Pop a friend from the queue and add to the list
        friend = queue.pop(0)
        # Get friends
        friends = getFriends(friend)
        for element in friends:
            username=element.get_name()
            if username not in friendlist:
                friendlist.append(username)
                i += 1
                queue.append(username)
    return friendlist



# defining various list for merging into the final .csv file
usernames = []
musictitle= []
artist  = []
playingtime= []
album = []
Userlist = BFS("rj", count1 ,friendlist=[] )



# gettig the user infor and then adding all the individual elements in temporary list in order to be dumped into final list
for user in Userlist:
    network = networkdeclaration(user)
    username = pylast.User(user, network)
    print username
    tracks = username.get_recent_tracks(limit= 200)
    musictemp = []
    artisttemp = []
    playtimetemp = []
    albumtemp = []
    count = 0
    itr = 0
    for trackname in tracks:
        count = count + 1
        musictemp.append(trackname.track.title)
        artisttemp.append(trackname.track.artist)
        playtimetemp.append(trackname.playback_date)
        albumtemp.append(trackname.album)
    for itr in range(count):
        if itr ==0:
            usernames.append(user)
        else:
            usernames.append("")
        musictitle.append(musictemp[itr].encode("utf-8"))
        artist.append(artisttemp[itr])
        playingtime.append(playtimetemp[itr].encode("utf-8"))
        if albumtemp[itr]== None:
            album.append(albumtemp[itr])
        else:
            album.append(albumtemp[itr].encode("utf-8"))
        itr = itr + 1

df= pd.DataFrame( data= {"Users" : usernames, "Songs" : musictitle, "Artists" : artist , "Playtime" : playingtime , "Album": album},
                   columns= ["Users","Songs","Artists", "Playtime", "Album"])

df.to_csv("Crawlers/users.csv",  sep=',')
