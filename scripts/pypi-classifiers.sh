#!/usr/bin/env bash

curl "https://pypi.org/classifiers/" | rg "<a href=\"/search/\?c" | awk '{print substr($0,index($0,">")+1)}' | sed 's/<\/a>//' | sort -u | jq -R -s "split(\"\n\")[:-1]" | tee pypi-classifiers.json

mv pypi-classifiers.json _meta
