#!/bin/bash
# This script builds all the dgpy-libs packages however, we previously used
# poetry and have since moved to uv, which supports `uv build --all` so
# this script may be not long for this world...
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
DGPY_LIBS_REPO_ROOT="$(dirname $DIR)"

cd $DGPY_LIBS_REPO_ROOT
pwd
LOCAL_DGPY_PACKAGES="${DGPY_LIBS_REPO_ROOT}/dgpy-packages"
mkdir -p "$LOCAL_DGPY_PACKAGES"

rm -rfv "${LOCAL_DGPY_PACKAGES}/latest" || true
mkdir -p "${LOCAL_DGPY_PACKAGES}/latest"

function build_pkg() {
    dirpath="$1"
    pkgname=$(basename "${dirpath}")
    echo "____________"
    echo "Pkg: ${pkgname} -- Dirpath: ${dirpath}"
    cd "${DGPY_LIBS_REPO_ROOT}/${dirpath}"
    uv build --wheel
    mkdir -p "${LOCAL_DGPY_PACKAGES}/${pkgname}"
    cp -v dist/* "${LOCAL_DGPY_PACKAGES}/${pkgname}"

    last=$(ls -ld dist/*.whl | awk '{print $9}' | sort --version-sort --field-separator=- | tail -n 1)
    echo "Latest wheel: ${last}"
    cp -v "${last}" "${LOCAL_DGPY_PACKAGES}/latest"

    echo "${last}" >>"${DGPY_LIBS_REPO_ROOT}/installthingy.sh"

    last=$(ls -ld dist/*.tar.gz | awk '{print $9}' | sort --version-sort --field-separator=- | tail -n 1)
    echo "Latest source-dist: ${last}"
    cp -v "${last}" "${LOCAL_DGPY_PACKAGES}/latest"

    echo "^^^^^^^^^^^"
}

function mkzip() {
    echo "_______"
    echo "ZIPPING"
    echo ""
    cd "${LOCAL_DGPY_PACKAGES}"

    cp ./latest ${DGPY_LIBS_REPO_ROOT}/dist -rfv
    cp -rfv ${DGPY_LIBS_REPO_ROOT}/dist ${DGPY_LIBS_REPO_ROOT}/install-test/dist

    cp ./latest ./dgpy-libs-latest -rvf
    zip -r dgpy-libs-latest.zip ./dgpy-libs-latest
    rm -rfv ./dgpy-libs-latest
    cd "${DGPY_LIBS_REPO_ROOT}"
    echo "^^^^^^^^^^^"
}

# install poetry if not installed and build wheel
#if [ ! "$( pip list | grep poetry )" ]; then
#    python -m pip install poetry
#fi
# build dgpy wheel and upload to S3
echo "Building and upload DGPY wheel"

# build_pkg "dgpy"

build_pkg "libs/xtyping"
build_pkg "libs/listless"
build_pkg "libs/fmts"
build_pkg "libs/funkify"
build_pkg "libs/aiopen"
build_pkg "libs/asyncify"
build_pkg "libs/h5"
build_pkg "libs/jsonbourne"
build_pkg "libs/lager"
build_pkg "libs/requires"
build_pkg "libs/shellfish"
mkzip
