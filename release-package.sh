#!/bin/bash
set -x  

# Release assets
curl -OL https://github.com/eko5624/nginx-nosni/raw/master/old.json
SHORT_DATE=$(date "+%Y%m%d")
SHORT_SHA=$(cat old.json  | jq -r '.mpv-git')
curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases \
  -d '{"tag_name": "$SHORT_DATE","name":"$SHORT_DATE","body":"Bump to mpv-player/mpv@$SHORT_SHA"}'
  
release_id=$(curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/$SHORT_DATE | jq -r '.id')
  
for f in git*.7z; do
  curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
    -X POST -H "Accept: application/vnd.github.v3+json" \
    -H "Content-Type: $(file -b --mime-type $f)" \
    https://uploads.github.com/repos/${GITHUB_REPOSITORY}/releases/$release_id/assets?name=$(basename $f) --data-binary @$f; 
done
