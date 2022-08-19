#!/bin/bash

# Copied and modified from https://github.com/jeffreytse/jekyll-deploy-action/blob/1ce0b36aeb585140ed9d54247de31474d4ac7ea8/providers/github.sh

set -euo pipefail

: "${REPOSITORY:=${GITHUB_REPOSITORY}}"
: "${BRANCH:=gh-pages}"
: "${ACTOR:=${GITHUB_ACTOR}}"

# Check if deploy to same branch
if [[ "${REPOSITORY}" = "${GITHUB_REPOSITORY}" ]]; then
  if [[ "${GITHUB_REF}" = "refs/heads/${BRANCH}" ]]; then
    echo "It's conflicted to deploy on same branch ${BRANCH}"
    exit 1
  fi
fi

echo "Deploying to ${REPOSITORY} on branch ${BRANCH}"
echo "Deploying to https://${ACTOR}:${TOKEN}@github.com/${REPOSITORY}.git"

REMOTE_REPO="https://${ACTOR}:${TOKEN}@github.com/${REPOSITORY}.git"

pushd _site

git init -b "${BRANCH}"
git config user.name "${ACTOR}"
git config user.email "${ACTOR}@users.noreply.github.com"
git remote add origin "${REMOTE_REPO}"
git fetch origin "${BRANCH}"
git reset "origin/${BRANCH}"
git add .
git commit -m "jekyll build from Action ${GITHUB_SHA}"
git push --force "$REMOTE_REPO" "$BRANCH"

popd
