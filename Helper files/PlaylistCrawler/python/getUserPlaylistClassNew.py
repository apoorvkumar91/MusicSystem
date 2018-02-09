import pylast
import pandas as pd
import random
import sys
import time

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

unique_sequence = uniqueid()


class getUserPlaylists(object):
   def __init__(self):
       # You have to have your own unique two values for API_KEY and API_SECRET
       # Obtain yours from http://www.last.fm/api/account/create for Last.fm
       self.API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
       self.API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
       self.output_file_location = "../data/users_playlist.csv"
       # defining various list for merging into the final .csv file
       self.usernames = []
       self.musictitle = []
       self.artist = []
       self.playingtime = []
       self.album = []
       self.tagslist = []
       self.particusercount = []
       self.tracklist = []
       self.particusercount=[]
       self.song_id_list=[]

   def networkdeclaration(self, username):
       network = pylast.LastFMNetwork(api_key=self.API_KEY, api_secret=self.API_SECRET,
                                      username=username, password_hash=None)
       return network


   def writeToCSV(self):
       df = pd.DataFrame(
           data={"Users": self.usernames, "Songs": self.musictitle, "Artists": self.artist, "Playtime": self.playingtime, "Album": self.album,

                 },
           columns=["Users", "Songs", "Artists", "Playtime", "Album"])

       # df = pd.DataFrame(
       #     data={"Users": self.usernames, "Songs": self.musictitle, "Artists": self.artist, "Playtime": self.playingtime, "Album": self.album,
       #
       #           "Tags": self.tagslist},
       #     columns=["Users", "Songs", "Artists", "Playtime", "Album", "Tags"])

       df.to_csv(self.output_file_location, sep=',')


   # gettig the user infor and then adding all the individual elements in temporary list in order to be dumped into final list
   def writeUserPlaylist(self, songlistlimit):
       count = 0
       for user in self.userlist:
           network = self.networkdeclaration(user)
           username = pylast.User(user, network)
           try:
               tracks = username.get_recent_tracks(limit=songlistlimit)
           except:
               print "Exception", user
               self.writeToCSV()
               continue
           for trackname in tracks:
               # try:
               #     thistrack = network.get_track(trackname.track.artist, trackname.track.title)
               # except:
               #     continue
               # try:
               #     tags = thistrack.get_top_tags(limit=200)
               # except:
               #     tags=[]
               # temptags = []
               # if tags==[]:
               #     self.tagslist.append(temptags)
               # else:
               #     for temp in tags:
               #         temptags.append(temp.item.get_name())
               #     self.tagslist.append(temptags)

               self.musictitle.append((trackname.track.title).encode("utf-8"))
               self.artist.append((trackname.track.artist))
               self.playingtime.append((trackname.playback_date).encode("utf-8"))
               albumtemp = trackname.album
               self.usernames.append(user)
               if albumtemp == None:
                   self.album.append(albumtemp)
               else:
                   self.album.append(albumtemp.encode("utf-8"))
               count = count + 1
       self.writeToCSV()

def main(args):
    #start_time= time.time()
    if len(args)<5:
        print("Please pass valid arguments")
        sys.exit(1)
    start=args[1]
    end= args[2]
    file_location = args[3]
    df = pd.read_csv(file_location)
    objectGetUsersPlaylist = getUserPlaylists()
    objectGetUsersPlaylist.output_file_location= args[4]
    objectGetUsersPlaylist.userlist= list(df.iloc[int(start):int(end), 1])
    objectGetUsersPlaylist.writeUserPlaylist(200)
    #print time.time()-start_time

if __name__ == "__main__": main(sys.argv)





