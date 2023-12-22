#!/bin/bash
set -x
CURL_RETRIES="--connect-timeout 60 --retry 5 --retry-delay 5 --http1.1"

#Get mpv latest commit sha
short_sha=$(cat /d/msys64/opt/mpv/SHORT_SHA)
date=$(date +%Y-%m-%d)

#Release note
body="Bump to mpv-player/mpv@${short_sha}\n"
body+="**Compiler**: clang"

curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases \
  -d '{"tag_name":"'"$date"'","name":"'"$date"'","body":"'"$body"'"}'
  
release_id=$(curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/$date | jq -r '.id')
  
for f in *.7z; do
  curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
    -X POST -H "Accept: application/vnd.github.v3+json" \
    -H "Content-Type: $(file -b --mime-type $f)" \
    https://uploads.github.com/repos/${GITHUB_REPOSITORY}/releases/$release_id/assets?name=$(basename $f) --data-binary @$f; 
done
