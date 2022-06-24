from time import time
from pathlib import Path
import os
import sqlite3
import re
from datetime import timezone, datetime
import sys
import requests


ROOT = 'api.listenbrainz.org'


p = Path('~').expanduser()


listenzFilePath = "/<CHANGE ME>/lastListenzFile.txt"
dbFilePath = "/<CHANGE ME>/AudirvanaPlusDatabaseV2.sqlite"

apiToken = "<CHANGE ME>"

MAX_LISTEN_SIZE = 5000


def submit_listen(listen_type, payload, token):
    """Submits listens for the track(s) in payload.

    Args:
        listen_type (str): either of 'single', 'import' or 'playing_now'
        payload: A list of Track dictionaries.
        token: the auth token of the user you're submitting listens for

    Returns:
         The json response if there's an OK status.

    Raises:
         An HTTPError if there's a failure.
         A ValueError is the JSON in the response is invalid.
    """

    tstJson = {
            "listen_type": listen_type,
            "payload": payload,
        }

    #print("Payload is "+str(tstJson))

    response = requests.post(
        url="https://{0}/1/submit-listens".format(ROOT),
        json={
            "listen_type": listen_type,
            "payload": payload,
        },
        headers={
            "Authorization": "Token {0}".format(token)
        }
    )

    response.raise_for_status()

    return response.json()


print("DB "+dbFilePath)

lastListenzFile = os.open(listenzFilePath, os.O_RDONLY | os.O_CREAT)
lastListenzBytes = os.read(lastListenzFile, 19)
lastListen = bytes.decode(lastListenzBytes, 'utf-8')
os.close(lastListenzFile)

if len(lastListen) <= 1:
    lastListen = "2459364.9074768517"

print("Last Listenbrainz listen? "+str(lastListen))


con = sqlite3.connect("file:"+dbFilePath+"?mode=ro", uri=True)
con.isolation_level = None

sql = """ select ARTISTS.name as artist, ALBUMS.title as album,TRACKS.year, TRACKS.title, date(TRACKS.last_played_date) as date, time(TRACKS.last_played_date) as time, last_played_date
 from TRACKS, ALBUMS, ALBUMS_ARTISTS, ARTISTS
 where ALBUMS.album_id = TRACKS.album_id and ALBUMS_ARTISTS.album_id = ALBUMS.album_id and ALBUMS_ARTISTS.artist_id = ARTISTS.artist_id
 and round(last_played_date,4) > round("""+lastListen+""",4)
 order by last_played_date asc """

cursorObj = con.cursor()
con.row_factory = lambda cursor, row: row[0]
cursorObj.execute(sql)
rows = cursorObj.fetchall()

rowNum = 0

currentPayloadSize = 0
listenzPayload = []

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
    #scrobble = network.scrobble(artist=artist, title=track, timestamp=unixTime, album_artist=artist, album=album)
    #json_response = submit_listen(listen_type='single', payload=EXAMPLE_PAYLOAD, token=apiToken)

    currentPayloadSize = sys.getsizeof(listenzPayload)

    if currentPayloadSize < MAX_LISTEN_SIZE: 
        print(str(rowNum)+": "+artist+" "+album+" "+track+" "+str(datePlay)+" "+str(timePlay)+" "+str(unixTime)+" "+str(lastPlay))
        track = {
          "listened_at": unixTime,
          "track_metadata": {
            "artist_name": artist,
            "track_name": track,
            "release_name": album
          }
        }
        lastListen = str(lastPlay)
        if sys.getsizeof(listenzPayload) > 0:
            listenzPayload.append(track)
        else:
            listenPayload = [
              track
            ]


#time.sleep(.900)

con.close

if currentPayloadSize > 0:
    #payload = [
    #  {
    #    "listen_type": import,
    #    "payload": [
    #        listenzPayload
    #    ]
    #  }
    #]
    #print("Payload is "+str(listenzPayload))
    json_response = submit_listen(listen_type='import', payload=listenzPayload, token=apiToken)
    print("Listenbrainz response was: {0}".format(json_response))

lastListenzFile = os.open(listenzFilePath, os.O_RDWR)
os.write(lastListenzFile, str.encode(lastListen, 'utf-8'))
os.close(lastListenzFile)

print("Done!")