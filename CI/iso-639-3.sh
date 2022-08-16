#!/bin/sh

cd data
rm -f iso-639-3.pck
wget -O iso-639-3.tab http://www-01.sil.org/iso639-3/iso-639-3.tab
python2 convert-iso-639-3.py
mv -f iso-639-3.pck py2
sleep 0.1
python3 convert-iso-639-3.py
mv -f iso-639-3.pck py3
sleep 1
cd ..

git add -u
git add *
git commit -m "Fetch latest iso-639-3 data."
