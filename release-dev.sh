#!/bin/bash
set -x


DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PATH="$DIR/bin:$PATH"
CURL=$DIR/bin/curl
# Delete assets
asset_id=$($CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/dev \
  | jq -r '.assets[] | select(.name | startswith("'"$1"'")) | .id') 
  
$CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X DELETE \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/assets/$asset_id    

# Release assets
$CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases \
  -d '{"tag_name": "dev"}'
  
release_id=$($CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/dev | jq -r '.id')
  
for f in $2/*.zst; do 
  $CURL -u $GITHUB_ACTOR:$GH_TOKEN $CURL_RETRIES \
    -X POST -H "Accept: application/vnd.github+json" \
    -H "Content-Type: $(file -b --mime-type $f)" \
    https://uploads.github.com/repos/${GITHUB_REPOSITORY}/releases/$release_id/assets?name=$(basename $f) --data-binary @$f; 
done
