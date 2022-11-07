#!/bin/bash
set -x

github_repository="eko5624/mpv-win64"

# Delete assets
asset_id=$(curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${github_repository}/releases/tags/dev \
  | jq -r --arg name "$1" '.assets[] | select(.name | startswith($name)) | .id') 
  
curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X DELETE \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${github_repository}/releases/assets/$asset_id    

# Release assets
curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${github_repository}/releases \
  -d '{"tag_name": "dev"}'
  
release_id=$(curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${github_repository}/releases/tags/dev | jq -r '.id')
  
for f in $2/*.zst; do 
  curl -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
    -X POST -H "Accept: application/vnd.github.v3+json" \
    -H "Content-Type: $(file -b --mime-type $f)" \
    https://uploads.github.com/repos/${github_repository}/releases/$release_id/assets?name=$(basename $f) --data-binary @$f; 
done
