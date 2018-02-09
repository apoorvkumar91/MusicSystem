import pylast
import pandas as pd
import random
import sys
import time
def uniqueid():
    #seed = random.getrandbits(32)
    seed=0
    while True:
       yield seed
       seed += 1




class getSongMetaData(object):
   def __init__(self):
       # You have to have your own unique two values for API_KEY and API_SECRET
       # Obtain yours from http://www.last.fm/api/account/create for Last.fm
       self.API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
       self.API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
       self.output_file_location = ""
       # defining various list for merging into the final .csv file
       self.usernames = []
       self.musictitle = []
       self.artist = []
       self.album = []
       self.tagslist = []
       self.listener_count=[]
       self.users_count=[]
       self.duration=[]
       self.song_id_list=[]
       self.meta_musictitle=[]
       self.meta_artist=[]
       self.meta_album=[]
       self.meta_song_id_list = []
       self.df=pd.DataFrame()
       self.unique_sequence = uniqueid()
       self.network=self.networkdeclaration("rj")

   def networkdeclaration(self, username):
       network = pylast.LastFMNetwork(api_key=self.API_KEY, api_secret=self.API_SECRET,
                                      username=username, password_hash=None)
       return network


   def writeToCSV(self):
       metadata_frame= pd.DataFrame(data={ "SongId": self.meta_song_id_list, "Songs": self.meta_musictitle, "Artists": self.meta_artist, "Album": self.meta_album, "listeners": self.listener_count, "users_playcount": self.users_count ,  "duration" : self.duration, "Tags": self.tagslist
                 },
           columns=[ "SongId","Songs", "Artists", "listeners", "users_playcount"  ,"duration", "Tags"])
       metadata_frame.to_csv(self.output_file_location, sep=",")
       self.df['SongId']= self.song_id_list
       self.df.sort_values(by=['Users', 'Playtime'], ascending=[True,True], inplace=True)
       self.df.to_csv("../data/users_playlist_new_copy.csv", sep=',')
   # gettig the user infor and then adding all the individual elements in temporary list in order to be dumped into final list
   def writeSongMetadata(self):
       #for

       def rountine(i):
           try:
               track = self.network.get_track(self.artist[i], self.musictitle[i])
           except:
               print "Exception", self.musictitle[i]
               self.writeToCSV()
           try:
               tags = track.get_top_tags(limit=200)
           except:
               tags = []
           temptags = []
           for temp in tags:
               temptags.append(temp.item.get_name())
           self.tagslist.append(temptags)
           self.meta_musictitle.append(self.musictitle[i])
           self.meta_album.append(self.album[i])
           self.meta_artist.append(self.artist[i])
           self.listener_count.append(track.get_listener_count())
           self.users_count.append(track.get_playcount())
           self.duration.append(track.get_duration())
           seqid = self.unique_sequence.next()
           self.meta_song_id_list.append((seqid))
           self.song_id_list.append((seqid))
       i=0
       rountine(i)
       for i in range(1,len(self.musictitle)):
           if self.artist[i]==self.artist[i-1] and self.musictitle[i]==self.musictitle[i-1]:
               self.song_id_list.append(self.song_id_list[i-1])
               continue
           rountine(i)
       self.writeToCSV()





def main(args):
    if len(args) < 3:
        print("Please pass valid arguments")
        sys.exit(1)
    start_time=time.time()
    file_location = args[1]


    objectGetSongMeta = getSongMetaData()
    objectGetSongMeta.df = pd.read_csv(file_location)
    # df.drop('Users', axis=1, inplace=True)
    # df.drop('Playtime', axis=1, inplace=True)
    objectGetSongMeta.df.sort_values(by=['Songs', 'Artists'], ascending=[True, True], inplace=True)
    objectGetSongMeta.musictitle = list(objectGetSongMeta.df["Songs"])
    objectGetSongMeta.output_file_location = args[2]
    objectGetSongMeta.artist = list(objectGetSongMeta.df["Artists"])
    objectGetSongMeta.album = list(objectGetSongMeta.df["Album"])
    objectGetSongMeta.writeSongMetadata()
    print "time elapsed", start_time-time.time()

if __name__ == "__main__": main(sys.argv)





