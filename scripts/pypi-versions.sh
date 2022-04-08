#!/usr/bin/env bash

# pip index versions shellfish | grep -i available | cat f.txt | cut -d' ' -f 3- | jq -R 'split(", ")'

pip index versions shellfish | grep -i available | cat f.txt | cut -d' ' -f 3- | jq -R 'split(", ")'

function pypi_versions(){
    echo $(pip index versions ${1} | grep -i available | cat f.txt | cut -d' ' -f 3- | jq -R 'split(", ")')
}

function pypi_versions_obj(){
    pkgname=$1
    echo $(pip index versions ${1} 2>/dev/null | grep -i available | cat f.txt | cut -d' ' -f 3- | jq -R "split(\", \") | {\"$pkgname\": .}")
}

pypi_versions shellfish

pypi_versions_obj shellfish
pypi_versions_obj jsonbourne


SHELLFISH=$(pypi_versions_obj shellfish)
JSONBOURNE=$(pypi_versions_obj jsonbourne)

echo $SHELLFISH $JSONBOURNE | jq -s add
