#!/usr/bin/env bash
set -e
# Pull requests and commits to other branches shouldn't try to decrypt the private key
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "master" ]; then
    exit 0
fi

openssl aes-256-cbc -K $encrypted_c7d371b9a595_key -iv $encrypted_c7d371b9a595_iv -in .private/deploy_key.enc -out .private/deploy_key -d
