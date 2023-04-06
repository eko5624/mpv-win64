#!/bin/bash
set -x
CURL_RETRIES="--connect-timeout 60 --retry 5 --retry-delay 5 --http1.1"
for param in "$@"; do
  download_url=($(curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/latest \
    | jq -r '.assets[] | select(.name | startswith("'"$param"'")) | .browser_download_url'));
  for url in "${download_url[@]}"; do
    curl -OL $url;
  done
done
pacman -U *.xz --noconfirm
