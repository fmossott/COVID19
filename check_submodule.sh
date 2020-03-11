#!/bin/bash -e

function banner {
  echo
  echo --------------------------------------------------------
  echo $1
  echo --------------------------------------------------------
  echo
}

cd `dirname $0`

# Merge pcm-dpc/COVID-19
banner "Merging pcm-dpc/COVID-19"

git checkout master
git submodule init
git pull --recurse-submodules
git submodule update --recursive --remote

if [[ `git status --porcelain` ]]; then
  echo incoming changes
  exit 0
else
  echo No changes to commit
  exit 1
fi
