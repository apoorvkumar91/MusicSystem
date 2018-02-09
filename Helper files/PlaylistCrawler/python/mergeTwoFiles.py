#packages and libraries
import pandas as pd

file_1 = 'Users/sidverma/Desktop/Final_Playlist_Users_0_1500.csv'
file_2='Users/sidverma/Desktop/Final_Playlist_Users_1500_3000.csv'
dfs=[]
df1=pd.read_csv(file_1)
df2=pd.read_csv(file_2)
df1.drop('Unnamed: 0',axis=1, inplace=True)
df2.drop('Unnamed: 0',axis=1, inplace=True)

dfs.append(df1)
dfs.append(df2)
frame= pd.concat(dfs)
frame=frame.reset_index(drop=True)

frame.to_csv('Users/sidverma/Desktop/Final_playlist_new.csv', sep=',')




