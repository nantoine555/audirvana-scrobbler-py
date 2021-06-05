import sqlite3
import pylast
import re
import time
from datetime import timezone, datetime
import os
from pathlib import Path


p = Path('~').expanduser()

# lastScrobbleFilePath = str(p) + "/tmp1/lastScrobbleFile.txt"
# dbFilePath = str(p) + "/tmp1/AudirvanaPlusDatabaseV2.sqlite"

lastScrobbleFilePath = "/<CHANGE ME>/lastScrobbleFile.txt"
dbFilePath = "/<CHANGE ME>/AudirvanaPlusDatabaseV2.sqlite"

print("DB "+dbFilePath)

#if not os.path.exists(lastScrobbleFilePath):
#    with open('lastScrobbleFilePath', os.O_CREAT): pass

lastScrobbleFile = os.open(lastScrobbleFilePath, os.O_RDONLY | os.O_CREAT)
lastScrobbleBytes = os.read(lastScrobbleFile, 19)
lastScrobble = bytes.decode(lastScrobbleBytes, 'utf-8')
os.close(lastScrobbleFile)

if len(lastScrobble) <= 1:
    lastScrobble = "2459364.9074768517"

print("Last Scrobble? "+str(lastScrobble))

#https://www.last.fm/api
ApiKey = "<CHANGE ME>"
ApiSecret = "<CHANGE ME>"
ApiUser = "<CHANGE ME>"
ApiPwd = pylast.md5("<CHANGE ME>")

network = pylast.LastFMNetwork(api_key=ApiKey, api_secret=ApiSecret,
                               username=ApiUser, password_hash=ApiPwd)

con = sqlite3.connect("file:"+dbFilePath+"?mode=ro", uri=True)
con.isolation_level = None

sql = """ select ARTISTS.name as artist, ALBUMS.title as album,TRACKS.year, TRACKS.title, date(TRACKS.last_played_date) as date, time(TRACKS.last_played_date) as time, last_played_date
 from TRACKS, ALBUMS, ALBUMS_ARTISTS, ARTISTS
 where ALBUMS.album_id = TRACKS.album_id and ALBUMS_ARTISTS.album_id = ALBUMS.album_id and ALBUMS_ARTISTS.artist_id = ARTISTS.artist_id
 and round(last_played_date,4) > round("""+lastScrobble+""",4)
 order by last_played_date asc """

#Sunday 9 Feb 2020, 6:40pm
#26 Jan 3:42pm

cursorObj = con.cursor()
con.row_factory = lambda cursor, row: row[0]
cursorObj.execute(sql)
rows = cursorObj.fetchall()

rowNum = 0

for row in rows:
    rowNum += 1
    artist = row[0]
    album = (re.sub('[\(\[].*?[\)\]]', '', row[1])).strip()
    year = row[2]
    track = row[3]
    datePlay = row[4]
    timePlay = row[5]
    lastPlay = row[6]
    dt = datetime.strptime(datePlay+" "+timePlay, "%Y-%m-%d %H:%M:%S")
    unixTime = dt.replace(tzinfo=timezone.utc).timestamp()
    print(str(rowNum)+": "+artist+" "+album+" "+track+" "+str(datePlay)+" "+str(timePlay)+" "+str(unixTime)+" "+str(lastPlay))
    scrobble = network.scrobble(artist=artist, title=track, timestamp=unixTime, album_artist=artist, album=album)

    lastScrobble = str(lastPlay)

    time.sleep(.900)

con.close

lastScrobbleFile = os.open(lastScrobbleFilePath, os.O_RDWR)
os.write(lastScrobbleFile, str.encode(lastScrobble, 'utf-8'))
os.close(lastScrobbleFile)

print("Done!")