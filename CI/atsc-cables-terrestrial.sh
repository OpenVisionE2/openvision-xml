#!/bin/sh

cd xml
wget -O atsc.xml https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/atsc.xml
wget -O cables.xml https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/cables.xml
wget -O terrestrial.xml https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/terrestrial.xml
cd ..

git add -u
git add *
git commit -m "Fetch latest OE-A's files."
