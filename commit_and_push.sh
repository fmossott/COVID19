#!/bin/sh  

cd `dirname $0`

. ./common

mergetime=`date -Iseconds -u` 

banner "Committing to 'Merge $mergetime'"

git commit -a -m "Merge $mergetime"
git push
