#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
DGPY_LIBS_REPO_ROOT="$(dirname $DIR)"
LIBS_DIR_PATH="$DGPY_LIBS_REPO_ROOT/libs"

ls "${LIBS_DIR_PATH}" | xargs -n1 -t uv version --bump patch --package
