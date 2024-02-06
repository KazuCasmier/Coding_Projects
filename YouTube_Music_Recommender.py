import ytmusicapi
import tkinter
import csv
import json

"""
Create a music recommender that takes the last 5-10 songs the user has listened to and takes the genre and mood
and gives an int value and increases the more often it appears in the listening history and will recommend songs
with the top 2-3 genres 

How I think its going to work:
- Take data from google takeout and filter by history of YT music
- Run through the data and take the genre and and mood and allocate it a counting variable that increases each time it 
    it appears
- Return a list of 5* songs that fit into the genres scraped
"""
yt_music_links = []

with open('music-library-songs.csv', 'r', newline='', errors='ignore') as file:
    read_csv_file = csv.reader(file)
    for row in read_csv_file:
        yt_music_links.append(row[0])

yt_music_links.pop(0)


history_links = []
history_json = open('watch-history.json', errors='ignore')

links = json.load(history_json)

for i in links:
    if 'titleUrl' in i:
        history_links.append(i['titleUrl'])
    else:
        break

comb_lst = []


for x in yt_music_links:
    for j in history_links:
        if j not in x:
            pass
        else:
            comb_lst.append(j)

print(comb_lst)

