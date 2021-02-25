#!/bin/sh

cd data
wget -O iso-639-3.tab http://www-01.sil.org/iso639-3/iso-639-3.tab
python convert-iso-639-3.py
sleep 1
cd ..
