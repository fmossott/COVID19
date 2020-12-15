#!/bin/bash

home=`dirname $0`

. $home/common

TGT_DIR="combined"
if [ ! -d $TGT_DIR ]; then
  mkdir $TGT_DIR
fi

# Apply patches
for f in patches/*.patch; do
  git -C COVID-19 apply ../$f
done

banner "Elaborating Regions data"
python3 pyscript/regiondata.py

banner "Elaborating Provinces data"
python3 pyscript/provincedata.py

# Remove patches
git -C COVID-19 reset --hard