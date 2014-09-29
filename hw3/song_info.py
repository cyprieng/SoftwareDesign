# -*- coding: utf-8 -*-
"""
Get the last played song (or the song currently playing), and show the 
original and french lyrics. Then show artist biography

@author: Cyprien Guillemot
"""

#IMPORT
import pylast
from pattern.web import URL
import wikipedia
import goslate

#Lastfm API KEY
API_KEY = "679472ce464ecfadc3d3a099649e0545"
API_SECRET = "1024a74f7846ed0fcfe6cdbfb2289452"

#Ask for lastfm username
username = raw_input("Lastfm username: ")

#Get last played track
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username =  username)
user = pylast.User(username,network=network)
last_scrobble = user.get_recent_tracks(limit=2)[0]
artist = str(last_scrobble.track.artist)
title =  str(last_scrobble.track.title)

#Get lyrics
lyrics = URL('http://api.ntag.fr/lyrics/?artist='+artist+'&title='+title).download()

#Translate in french
gs = goslate.Goslate()
lyricsFR = gs.translate(lyrics, 'fr')

#Get biography
bio = wikipedia.summary(artist, sentences=2)

#PRINT
print '\n'+title+" - "+artist
print "-----------------"

#Print lyrics in two columns
for line1, line2 in zip(lyrics.split('\n'), lyricsFR.split('\n')):
    print "%s %s" % (line1.ljust(100), line2)

print '\n'+artist
print "-----------------"
print bio
