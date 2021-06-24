#!/bin/sh

cd xml
python lyngsat.py
sleep 1
cd ..

git add -u
git add *
git commit -m "Fetch latest lyngsat files."
