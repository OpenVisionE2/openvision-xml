#!/bin/sh

get_files() {
  cd data
  wget -O iso-639-3.tab http://www-01.sil.org/iso639-3/iso-639-3.tab
  python convert-iso-639-3.py
  cd ..
  mv -f *.xml xml
  cd xml
  wget -O atsc.xml https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/atsc.xml
  wget -O cables.xml https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/cables.xml
  wget -O terrestrial.xml https://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/terrestrial.xml
  cd ..
}

setup_git() {
  git config --global user.email "bot@openvision.tech"
  git config --global user.name "Open Vision bot"
}

commit_files() {
  git checkout master
  git add -u
  git add *
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add upstream https://${GH_TOKEN}@github.com/OpenVisionE2/openvision-xml.git > /dev/null 2>&1
  git push --quiet upstream master || echo "failed to push with error $?"
}

setup_git
get_files
commit_files
upload_files
