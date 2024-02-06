import tkinter
import csv
import json
import ytmusicapi

"""
Create a music recommender that takes the last 5-10 songs the user has listened to and takes the genre and mood
and gives an int value and increases the more often it appears in the listening history and will recommend songs
with the top 2-3 genres 

How I think its going to work:
- Take data from google takeout and filter by history of YT music ---- DONE
- Run through the data and take the genre and and mood and allocate it a counting variable that increases each time it 
    it appears
- Return a list of 5* songs that fit into the genres scraped
"""
# Every list needed to make this work (I think)
yt_music_links = []
comb_lst = []
history_links = []

# Opens the music library and returns a list of strings
with open('music-library-songs.csv', 'r', newline='', errors='ignore') as file:
    read_csv_file = csv.reader(file)
    for row in read_csv_file:
        yt_music_links.append(row[0])
yt_music_links.pop(0)

# Opens and loads the .json file with the YT watch history
history_json = open('watch-history.json', errors='ignore')

links = json.load(history_json)

# Puts all the YT links into a list
for i in links:
    if 'titleUrl' in i:
        history_links.append(i['titleUrl'])
    else:
        break

# Makes a combined list that filters out regular YT videos by recently listened to
for x in history_links:
    for j in yt_music_links:
        if j not in x:
            pass
        else:
            comb_lst.append(j)

print(comb_lst)


class BrowsingMixin:
    def __init__(self):

        pass

    def get_song(self):
        ytmusicapi.YTMusic.get_song(self, videoId=comb_lst[0], signatureTimestamp=0)


test = BrowsingMixin()

test.get_song()
