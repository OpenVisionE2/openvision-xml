#!/bin/sh

cd xml
python TimeZoneUpdater.py 7KZU8BFJBHD8 timezone.xml
sleep 1
cd ..

git add -u
git add *
git commit -m "Fetch latest IANA's timezone changes."
