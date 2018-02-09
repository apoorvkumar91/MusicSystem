import pylast
import pandas as pd

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account/create for Last.fm
API_KEY = "1eda1ba7ac590388343743dcebada5ee"  # this is a sample key
API_SECRET = "ce4e1b7a740a8107afa60152eea43b32"
count=200
output_file_location= "../data/users.csv"

def getFriends(friend):
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                   username=friend, password_hash=None)
    user = pylast.User(friend, network)
    friends = user.get_friends(10, True)
    return friends



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
            if [username] not in friendlist:
                friendlist.append([username])
                i += 1
                queue.append(username)
    return friendlist



#Fecth Friends beginning from user with username="rj"
df = pd.DataFrame(BFS("rj", count ,friendlist=[] ))
df.to_csv("../data/users.csv",  sep=',')

