#!/bin/sh -e

function fail {
  echo $1
  exit 1
}

cd `dirname $0`

. ./common

git checkout master
if [ "$1" != "--nopull" ]; then
  banner "Merging project"
  git pull
fi

# Merge pcm-dpc/COVID-19
banner "Merging pcm-dpc/COVID-19"

#git submodule update --init
#git pull --recurse-submodules
#git submodule update --recursive --remote

git -C COVID-19 checkout master
git -C COVID-19 pull

# Combine reginonal data
./combine.sh

if [[ `git status --porcelain` ]]; then
  echo Changes to commit
  mergetime=`date -u "+%Y-%m-%dT%H:%M:%S"` 
  banner "Committing to 'Merge $mergetime'"
  git commit -a -m "Merge $mergetime"

  git push
  if [ -f refresh.sh ]; then
    ./refresh.sh
  fi
else
  echo No changes to commit
fi
