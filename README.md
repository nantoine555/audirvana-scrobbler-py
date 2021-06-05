# audirvana-scrobbler-py

To make it work:

1) Modify the paths in scrobble.py

lastScrobbleFilePath = "/<CHANGE ME>/lastScrobbleFile.txt"
dbFilePath = "/<CHANGE ME>/AudirvanaPlusDatabaseV2.sqlite"
  
The last Scrobble is a simple .txt file that is used to store the last scrobble time, to prevent a full database scan
The dbFilePath is by default on a mac: 

"$HOME/Library/Application Support/Audirvana/AudirvanaDatabase.sqlite" (Audirvana 3.5)
"$HOME/Library/Application Support/Audirvana/AudirvanaPlusDatabaseV2.sqlite" (Audirvana Studio 1.3)
  
Go to the last.FM Api page, register an API Account and fill the informations
#https://www.last.fm/api
ApiKey = "<CHANGE ME>"
ApiSecret = "<CHANGE ME>"
ApiUser = "<CHANGE ME>"
ApiPwd = pylast.md5("<CHANGE ME>")
  
2) i have provided an install.sh script that installs python 3.9.5 (on a mac) but you will need the following Python libs:

pip3 install pylast --user 
pip3 install certifi --user
  
 3) Catalina messed up my plist scheduler, but I used Automator to create a new Application that runs a shell script:
 /bin/sh -c "exec $HOME/bin/scrobble.sh"
 

 Disclaimers:
 
- BACKUP YOUR DATA (It won't touch your music files, just the Audirvana database) 
- NOT TESTED ON WINDOWS
- NOT TESTED ON ANOTHER MAC
- I WON’T PROVIDE 24x7 SUPPORT :wink:
- IT IS UNSUPPORTED BY DAMIEN/ANY AUDIRVANA PEOPLE (of course I will retire this if they offer native Last.FM Scrobbling in Audirvana Studio)

Do not complain if it destroys your database. I’m making a copy from the mac NVME disk to another ssd before reading the data, and so far no problem, but, sh*t happens, and if you are not at ease with computers, scripts and programming this thing may not be for you.
