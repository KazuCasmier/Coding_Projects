import tkinter
import csv
import json
import ytmusicapi
from ytmusicapi import YTMusic

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


ytmusicapi.YTMusic()


class BrowsingMixin:
    def __init__(self):
        ytmusicapi.setup(filepath='headers.txt', headers_raw='POST: /youtubei/v1/browse?key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30&prettyPrint=false HTTP/2 Host: music.youtube.com User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0 Accept: */* Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate, br Content-Type: application/json Content-Length: 2430 Referer: https://music.youtube.com/library X-Goog-Visitor-Id: Cgs5a29rMXBQQWw5USjypKCuBjIKCgJVUxIEGgAgaQ%3D%3D X-Youtube-Bootstrap-Logged-In: true X-Youtube-Client-Name: 67 X-Youtube-Client-Version: 1.20240205.00.00 X-Goog-AuthUser: 0 X-Origin: https://music.youtube.com Origin: https://music.youtube.com Sec-Fetch-Dest: empty Sec-Fetch-Mode: same-origin Sec-Fetch-Site: same-origin Authorization: SAPISIDHASH 1707610739_a46d84fa3a9b72371074bbddd1cbe43b22236aed Connection: keep-alive Cookie: VISITOR_INFO1_LIVE=9kok1pPAl9Q; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgaQ%3D%3D; PREF=f6=40000080&tz=America.Chicago; _gcl_au=1.1.329407250.1707283256; __Secure-1PSIDTS=sidts-CjEBPVxjSq7QVPs96lfkcG1ufo6DsEoDEwcfN5IgOCWelDMR9j0r5RZP-4a0SWVbghhUEAA; __Secure-3PSIDTS=sidts-CjEBPVxjSq7QVPs96lfkcG1ufo6DsEoDEwcfN5IgOCWelDMR9j0r5RZP-4a0SWVbghhUEAA; HSID=AZMJZeyf7N44RQ6LK; SSID=Au5YYmpupwGLfVHy9; APISID=x1douICWDHmAYUtB/AuSw4sWo-oHaSF40K; SAPISID=YmLyXhnhfDWN15t9/AiHVG5BRTURBzkqkB; __Secure-1PAPISID=YmLyXhnhfDWN15t9/AiHVG5BRTURBzkqkB; __Secure-3PAPISID=YmLyXhnhfDWN15t9/AiHVG5BRTURBzkqkB; SID=g.a000gAh1Jp7fIGNn1cHe4eKN1Wpa85q-NnRm4ISJQF6dURVx9wg7Uqc9fEe_IIavyVWnfP8wRAACgYKATgSAQASFQHGX2Mil07dz44XgVUBMXnJaCk0PBoVAUF8yKrnn3jQ89-7IN9_sWXQBZxd0076; __Secure-1PSID=g.a000gAh1Jp7fIGNn1cHe4eKN1Wpa85q-NnRm4ISJQF6dURVx9wg7kBbV6fD2PihKEdmOCXrctgACgYKAaISAQASFQHGX2MicbGx_dmJ4QfQ7Ll_onJDshoVAUF8yKp-_wZW2QvBSmwCv7yD0YfC0076; __Secure-3PSID=g.a000gAh1Jp7fIGNn1cHe4eKN1Wpa85q-NnRm4ISJQF6dURVx9wg7KPhVkKRsH4SNLL5N1P4UVQACgYKAUkSAQASFQHGX2MiT-amcIjOB1d5eHt7BVgZ9xoVAUF8yKoqrpavmT6_KUIxuEUiadqb0076; LOGIN_INFO=AFmmF2swRQIgDBPUHTNvfU2lXDRPf0LEG1cA3HdI9uisiK7lNG2HfMICIQD3Svb0Rk0goMeMn5cbMJfel4eY0m5OGKOU6q_LU0kkiw:QUQ3MjNmeTVVa09yZHo4WU1FeXBtSGtpRlNPQlFvd3RMOG5KWkpxNVg5d2c2TkM5dmJsQ3liU1RIVVhaWlNFbXdHazJnd0F1Um4xcFRldUFpU2V1T1l2Q1Vtb1BvTDlxQ3lIQ2pCNzE1c0pLSkRyX3NqdXJON1BydWRpaVNXeTJYN3NxUXlTbEhkNHVieGh2bldFNXNxblpJTnliRWdKV0tn; SIDCC=ABTWhQGGDpNzvyp1XSpztxuU2yWdyF5IF1RxXOzTRM_GqLLX14uTou7IBg7FkIzOiIaoLXbMsw; __Secure-1PSIDCC=ABTWhQEwOE7_Wgo-Hcb8ZN5fMw-6c9rLSGO1hhtydU6ceq2jbmzemOmS4Cdg-yNgtjMXj_z_ew; __Secure-3PSIDCC=ABTWhQGd1_BDgvHA12BznXu91N42X-DUUw2k10obnFkU3m1vuig6a2IIjJjs2GA8nz_n1N0OkA; YSC=FJ2uRW7RT6s TE: trailers')

    def get_song(self):
        print(ytmusicapi.YTMusic.get_song(self, videoId=comb_lst[0], signatureTimestamp=0))


test = BrowsingMixin()
test.__init__()