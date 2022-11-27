#!/bin/bash
set -x

download_url=($(curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/dev \
  | jq -r '.assets[] | select(.name | startswith("'"$1"'")) | .browser_download_url'))

for url in "${download_url[@]}"; do
  curl -OL $url;
done
  
  
