#!/bin/bash

function banner {
  echo
  echo -------------------------
  echo $1
  echo -------------------------
  echo
}

function fail {
  echo $1
  exit 1
}

function combine {
  tgt=$1
  shift
  
  banner Combining $* in $tgt

  first=true
  for f in $*; do
    if [ ! -f $f ]; then
      fail "$f does not exist"
    fi 
    echo adding $f to $tgt
    if $first ; then
      head -n1 $f > $tgt
      first=false
    fi
    tail -n+2 $f >> $tgt
  done
}

TGT_DIR="combined"
if [ ! -d $TGT_DIR ]; then
  mkdir $TGT_DIR
fi

# Combine reginonal data
combine $TGT_DIR/regioni.csv addons-dati-regioni/aaa-* COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv

