#!/bin/bash -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 <yyyymmdd>"
  exit 2
fi

cd `dirname $0`

. ./common

# Merge pcm-dpc/COVID-19
banner "Merging pcm-dpc/COVID-19"

git checkout master
git submodule init
git pull --recurse-submodules
git submodule update --recursive --remote

if [ -f COVID-19/dati-regioni/dpc-covid19-ita-regioni-$1.csv ]; then
  echo "today's data available"
  exit 0
elif [[ `git status --porcelain` ]]; then
  echo "incoming changes, but no new data"
  exit 1
else
  echo "No changes to commit"
  exit 1
fi
