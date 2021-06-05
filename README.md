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
 
