#!/usr/bin/env bash


SCRIPTS_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
DGPY_LIBS_REPO_ROOT=$(dirname "$SCRIPTS_DIR")

jq -c -r '.[]' ${DGPY_LIBS_REPO_ROOT}/_data/topo.json | while read i; do
    echo "$i"
    LIB_DIRPATH="${DGPY_LIBS_REPO_ROOT}/libs/${i}"
    echo "Updating ${i} ~ ${LIB_DIRPATH}"
    cd ${LIB_DIRPATH}
    poetry update
done

cd ${DGPY_LIBS_REPO_ROOT}
poetry update
