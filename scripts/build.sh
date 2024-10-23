#!/usr/bin/env bash

preflight() {
  # Check if jq is installed
  if ! command -v jq &>/dev/null; then
    echo "jq is not installed. Please install jq before running this script."
    exit 1
  fi

  # Check if hatch is installed
  if ! command -v hatch &>/dev/null; then
    echo "hatch is not installed. Please install hatch before running this script."
    exit 1
  fi
  mkdir -p ./dist
  rm -rf ./dist/*
}

build_metadata() {
  # Get data for archive...
  DGPY_LIBS_GIT_HASH=$(git -C . rev-parse HEAD)
  TIMESTAMP_UTC=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  # Construct JSON data using jq
  JSON_DATA=$(jq -n \
    --arg timestamp "$TIMESTAMP_UTC" \
    --arg dgpy_libs "$DGPY_LIBS_GIT_HASH" \
    '{timestamp: $timestamp, "dgpy-dev": $dgpy_dev, "dgpy-libs": $dgpy_libs}')

  echo "$JSON_DATA" >./dist/build.json
}

build_lib() {
  libname=$1
  cd "./libs/$libname" || exit 1
  if [ -d "./dist" ]; then
    rm -rf ./dist
  fi
  hatch build
  cp ./dist/* ../../dist
  cd ../..
}

build() {
  for dir in ./libs/*; do
    if [ -d "$dir" ]; then
      libname=$(basename "$dir")
      build_lib "$libname"
    fi
  done
}

main() {
  preflight
  build_metadata
  build
}

main
