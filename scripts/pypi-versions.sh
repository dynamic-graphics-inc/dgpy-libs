#!/usr/bin/env bash

DGPY_LIBS=(aiopen  asyncify  fmts  funkify  h5  jsonbourne  lager  listless  requires  shellfish  xtyping)

function pypi_versions(){
    echo $(pip index versions ${1} | grep -i available | cat f.txt | cut -d' ' -f 3- | jq -R 'split(", ")')
}

function pypi_versions_obj(){
    pkgname=$1
    vobj=$(pip index versions ${1} 2>/dev/null | grep -i available | cat f.txt | cut -d' ' -f 3- | jq -R "split(\", \") | {\"$pkgname\": .}")
    echo $vobj
}

function pypi_versions_obj_task(){
    pkgname=$1
    echo $(pypi_versions_obj $pkgname)
}

function main(){
    mkdir -p temp
    for i in "${DGPY_LIBS[@]}";do
        pypi_versions_obj_task "$i" > "temp/$i.json" &
    done;
    wait;
    echo "Pkg versions downloaded!"
    cat temp/* | jq -s add | jq -S > "_meta/pypi-pkg-versions.json"

    echo "__versions__"
    cat _meta/pypi-pkg-versions.json | jq -c
    echo "__latest__"
    cat _meta/pypi-pkg-versions.json | jq  'map_values(.[0])' | tee _meta/pypi-pkg-latest.json
}

main
