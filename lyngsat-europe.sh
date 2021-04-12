#!/bin/sh

cd xml
python lyngsat.py -r europe -f satellites-europe.xml
sleep 1
cd ..
