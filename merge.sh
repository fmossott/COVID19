#!/bin/bash -e

function banner {
  echo
  echo --------------------------------------------------------
  echo $1
  echo --------------------------------------------------------
  echo
}

function fail {
  echo $1
  exit 1
}

cd `dirname $0`

# Merge pcm-dpc/COVID-19
banner "Merging pcm-dpc/COVID-19"

git checkout master
git submodule init
git pull --recurse-submodules
git submodule update --recursive --remote

# Combine reginonal data
./combine.sh

mergetime=`date -Iseconds -u` 
banner "Committing to 'Merge $mergetime'"
git commit -a -m "Merge $mergetime"

if [[ `git status --porcelain` ]]; then
  echo Changes to push
  git push
  if [ -f refresh.sh ]; then
    refresh.sh
  fi
else
  echo No changes to push
fi
