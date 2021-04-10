#!/bin/bash

jupyter nbconvert --to markdown --execute "./README.ipynb"
#rm docs/index.md
cp README.md docs/index.md


while read -d '' filename; do
    echo "${filename}"
    jupyter nbconvert --to markdown --execute "${filename}"
    cp --parents "${filename}" docs
done < <(find "libs" -maxdepth 3 -type f -name "README.ipynb" -print0)
