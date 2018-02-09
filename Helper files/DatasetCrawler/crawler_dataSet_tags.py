import pylast
import pandas as pd
import re

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account/create for Last.fm
API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
count1=200
output_file_location= "Crawlers/users.csv"

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
length = len(df2)
network = networkdeclaration("rj")
for i in range(14000,14750):
    print i 
    track = network.get_track(ArtistFrame[i],SongsFrame[i])
    tags = track.get_top_tags(limit = 50)
    temptags = []
    for temp in tags:
        temptags.append(temp.item.get_name())
    tagslist.append(temptags)
    songtemp.append(SongsFrame[i])

df = pd.DataFrame( data = {"songs": songtemp , "tags" : tagslist,},
                   columns = ["songs","tags"])


#df= pd.DataFrame( data= {"Users" : usernames, "Songs" : musictitle, "Artists" : artist , "Playtime" : playingtime , "Album": album, "Tags" : tagslist},
 #                  columns= ["Users","Songs","Artists", "Playtime", "Album", "Tags"])

df.to_csv("Crawlers/users.csv",  sep=',')
