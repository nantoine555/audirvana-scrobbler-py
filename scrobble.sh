#!/bin/bash

dest="/<CHANGE ME>/AudirvanaPlusDatabaseV2.sqlite"
src="/<CHANGE ME>/AudirvanaDatabase.sqlite"

echo "Copying Audirvana DB from $src to $dest"
time cp -v "$src" "$dest"
echo "DB copied is $dest, running scrobbler"
/Library/Frameworks/Python.framework/Versions/Current/bin/python3 $HOME/bin/scrobble.py

echo "Purge DB from $dest"
rm -f "$dest"
echo "Done `date`"
