#!/bin/sh -e

if [ $# -lt 1 ]; then
  d=`date +%Y%m%d`
else
  d=$1
fi

cd `dirname $0`

. ./common

# Merge pcm-dpc/COVID-19
banner "Merging pcm-dpc/COVID-19"

git checkout master
#git submodule init
#git pull --recurse-submodules
#git submodule update --recursive --remote

git -C COVID-19 checkout master
if [[ `git -C COVID-19 status --porcelain` ]]; then
  git -C COVID-19 rm --cached -r .
  git -C COVID-19 reset --hard
fi
git -C COVID-19 pull

if [ -f COVID-19/dati-regioni/dpc-covid19-ita-regioni-$d.csv ]; then
  echo "today's data available"
  exit 0
elif [[ `git status --porcelain` ]]; then
  echo "incoming changes, but no new data"
  exit 1
else
  echo "No changes to commit"
  exit 1
fi
