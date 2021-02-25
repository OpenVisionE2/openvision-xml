#!/bin/sh

cd xml
python TimeZoneUpdater.py ${TimezonesDB_API} timezone.xml
sleep 1
cd ..
