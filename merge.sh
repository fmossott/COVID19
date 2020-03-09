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

md5sum combined/* > combined.md5

# Combine reginonal data
./combine.sh

md5sum --check combined.md5

if [ $? ]; then
  echo Combined has not changed
else
  mergetime=`date -Iseconds -u` 
  banner "Committing to 'Merge $mergetime'"
  git commit -a -m "Merge $mergetime"
fi

if [[ `git status --porcelain` ]]; then
  echo Changes to push
  git push
  if [ -f refresh.sh ]; then
    refresh.sh
  fi
else
  echo No changes to push
fi
