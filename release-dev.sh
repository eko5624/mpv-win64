#!/bin/bash
set -x

# Delete assets
asset_id=$(curl \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${{ github.token }}" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/dev \
  | jq -r '.assets[] | select(.name | startswith("'"$1"'")) | .id') 
  
curl \
  -X DELETE \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${{ github.token }}" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/assets/$asset_id    

# Release assets
curl \
  -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${{ github.token }}" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases \
  -d '{"tag_name": "dev"}'
  
release_id=$(curl \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ${{ github.token }}" \
  https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/dev | jq -r '.id')
  
for f in $2/*.zst; do 
  curl \
    -X POST -H "Accept: application/vnd.github.v3+json" \
    -H "Authorization: token ${{ github.token }}" \
    -H "Content-Type: $(file -b --mime-type $f)" \
    https://uploads.github.com/repos/${GITHUB_REPOSITORY}/releases/$release_id/assets?name=$(basename $f) --data-binary @$f; 
done
