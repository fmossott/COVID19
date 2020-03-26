#!/bin/bash

home=`dirname $0`

. $home/common

TGT_DIR="combined"
if [ ! -d $TGT_DIR ]; then
  mkdir $TGT_DIR
fi

banner "Elaborating Regions data"
python3 pyscript/regiondata.py

banner "Elaborating Provinces data"
python3 pyscript/provincedata.py

