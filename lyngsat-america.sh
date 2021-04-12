#!/bin/sh

cd xml
python lyngsat.py -r america -f satellites-america.xml
sleep 1
cd ..
