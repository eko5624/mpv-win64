#!/bin/bash
set -x  
CURL=/d/ucrt64/bin/curl

#Get mpv latest commit sha
short_sha=$(cat /d/msys64/opt/mpv/SHORT_SHA)

# Release assets
date=$(date +%Y-%m-%d)

$CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases \
  -d '{"tag_name":"'"$date"'","name":"'"$date"'","body":"Bump to mpv-player/mpv@'"$short_sha"'"}'
  
release_id=$($CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/$date | jq -r '.id')
  
for f in *.7z; do
  $CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
    -X POST -H "Accept: application/vnd.github.v3+json" \
    -H "Content-Type: $(file -b --mime-type $f)" \
    https://uploads.github.com/repos/${GITHUB_REPOSITORY}/releases/$release_id/assets?name=$(basename $f) --data-binary @$f; 
done
