import pylast
import pandas as pd
import re

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account/create for Last.fm
API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
count1=200
output_file_location= "Crawlers/latusers.csv"

def networkdeclaration(username):
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                   username=username, password_hash=None)
    return network

DataSet_file = "Crawlers/DataSet.csv"
df2 = pd.read_csv(DataSet_file)
SongsFrame = df2["Songs"]
ArtistFrame = df2["Artists"]
songtemp = []
tagslist = []
listener_count = []
users_count = []
particusercount = []
duration = []
length = len(df2)
network = networkdeclaration("rj")
for i in range(0,14750):
    print i 
    track = network.get_track(ArtistFrame[i],SongsFrame[i])
    listener_count.append(track.get_listener_count())
    users_count.append(track.get_playcount())
    particusercount.append(track.get_userplaycount())
    duration.append(track.get_duration())
   # temptags = []
   # for temp in tags:
    #    temptags.append(temp.item.get_name())
    #tagslist.append(temptags)
    songtemp.append(SongsFrame[i])

df = pd.DataFrame( data = {"songs": songtemp , "listeners": listener_count, "users_playcount": users_count , "particusercount" : particusercount, "duration" : duration},
                   columns = ["songs","listeners", "users_playcount" , "particusercount" ,"duration"])


#df= pd.DataFrame( data= {"Users" : usernames, "Songs" : musictitle, "Artists" : artist , "Playtime" : playingtime , "Album": album, "Tags" : tagslist},
 #                  columns= ["Users","Songs","Artists", "Playtime", "Album", "Tags"])

df.to_csv("Crawlers/latusers.csv",  sep=',')
