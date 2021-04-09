#!/bin/bash

while read -d '' filename; do
    echo "${filename}"
#    cp --parents "${filename}" docs
    jupyter nbconvert --to markdown --execute "${filename}"
done < <(find "libs" -maxdepth 3 -type f -name "README.ipynb" -print0)
