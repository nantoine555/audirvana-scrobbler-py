#!/bin/bash

cp -v com.karkoz.audirvana.scrobbler.plist $HOME/Library/LaunchAgents/
echo "Agent copied to $HOME/Library/LaunchAgents/"
mkdir -p $HOME/bin/
mkdir -p $HOME/tmp/

curl https://www.python.org/ftp/python/3.9.5/python-3.9.5-macosx10.9.pkg -o $HOME/python-3.9.5-macosx10.9.pkg

sudo installer -pkg $HOME/python-3.9.5-macosx10.9.pkg -target /
sudo sh "/Applications/Python 3.9/Install Certificates.command"

rm -f $HOME/python-3.9.5-macosx10.9.pkg

cp -v scrobble.sh $HOME/bin/scrobble.sh
cp -v scrobble.py $HOME/bin/scrobble.py
chmod a+x $HOME/bin/scrobble.sh

pip3 install pylast --user 
pip3 install certifi --user

echo "Intalled"

launchctl load $HOME/Library/LaunchAgents/com.karkoz.audirvana.scrobbler.plist

echo "Loaded, logs are available in /tmp/com.karkoz.audirvana.scrobbler.*.txt"
