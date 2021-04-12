#!/bin/sh

cd xml
python lyngsat.py -r atlantic -f satellites-atlantic.xml
sleep 1
cd ..
