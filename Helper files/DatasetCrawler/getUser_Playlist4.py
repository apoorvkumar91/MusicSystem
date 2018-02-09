import pylast
import pandas as pd
import random
import sys
import time
import threading


class myThread(threading.Thread):
   def __init__(self,FileNumber,startime,endtime):
       threading.Thread.__init__(self)
       # You have to have your own unique two values for API_KEY and API_SECRET
       # Obtain yours from http://www.last.fm/api/account/create for Last.fm
       self.API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
       self.API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
       self.output_file_location = "~/Desktop/Out/user_playlist_new_"+ str(FileNumber)+".csv"
       self.file_location = "/Users/sidverma/Documents/GitHub/CS670MyTunes/Datasets/Lastfm/Users_6000/users_playlist_new_0_1500.csv"
       # defining various list for merging into the final .csv file
       self.usernames = []
       self.musictitle = []
       self.startime = startime
       self.endtime = endtime
       self.artist = []
       self.playingtime = []
       self.album = []
       self.tagslist = []
       self.listenercount = []
       self.FileNumber = FileNumber
       self.tracklist = []
       self.playcount=[]
       self.duration = []
       self.song_id_list=[]
       self.SongsFrame = []
       self.ArtistFrame=[]
       self.songscount = []
       
   def run(self):
       df = pd.read_csv(self.file_location)
       self.SongsFrame = df["Songs"]
       self.ArtistFrame = df["Artists"]
       self.writeUserPlaylist()
       print "exiting"

   def networkdeclaration(self, username):
       network = pylast.LastFMNetwork(api_key=self.API_KEY, api_secret=self.API_SECRET,
                                      username=username, password_hash=None)
       return network

   def writeToCSV(self):
       df2 = pd.DataFrame(
           data={"Songs": self.songscount , "Tags" : self.tagslist, "Listeners": self.listenercount , "Playcount": self.playcount, "Duration" : self.duration,
                 },columns=["Songs","Listeners","Playcount","Duration", "Tags"])
       # df = pd.DataFrame(
       #     data={"Users": self.usernames, "Songs": self.musictitle, "Artists": self.artist, "Playtime": self.playingtime, "Album": self.album,
       #
       #           "Tags": self.tagslist},
       #     columns=["Users", "Songs", "Artists", "Playtime", "Album", "Tags"])

       df2.to_csv(self.output_file_location, sep=',')
   # gettig the user infor and then adding all the individual elements in temporary list in order to be dumped into final list
   def writeUserPlaylist(self):
       network = self.networkdeclaration("rj")
       for i in range(self.startime,self.endtime):
          track = network.get_track(self.ArtistFrame[i],self.SongsFrame[i])
          try:
             tags = track.get_top_tags(limit = 50)
          except:
             print "Exception"
             self.writeToCSV()
             self.output_file_location="~/Desktop/Out/Error_1_"+ str(self.FileNumber)+".csv"
             continue
          temptags = []
          for temp in tags:
              temptags.append(temp.item.get_name())
          self.tagslist.append(temptags)
          self.listenercount.append(track.get_listener_count())
          self.playcount.append(track.get_playcount())
          self.duration.append(track.get_duration())
          self.songscount.append(self.SongsFrame[i])
       self.writeToCSV()
threads = []
for itr in range(91,120):
  threads.append(myThread(itr,itr*1000,(itr+1)*1000))
print "I am going"
for itr in range(0,30):
   threads[itr].start()