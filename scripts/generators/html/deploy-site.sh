#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

SOURCE_BRANCH="master"
TARGET_BRANCH="gh-pages"

build_dir=".dist/html"

function log {
    echo "[$(date --rfc-3339=seconds)]: $*" >&2
}

function doCompile {
    dist_dir=${1:-.dist}
    log "Building HTML to ${dist_dir}"
    mkdir -p "${dist_dir}"
    pwd
    script_dir=$(cd $(dirname $0) && pwd)

    log "Compiling site template..."
    env PYTHONPATH=${script_dir}/../../:${PYTHONPATH} python ${script_dir}/generate.py "${script_dir}/templates/" "datafiles/streams/" "${dist_dir}"

    log "Copying static files..."
    cp -r ${script_dir}/static/* "${dist_dir}/"
}

# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy; just doing a build."
    doCompile "${build_dir}"
    exit 0
fi

# Save some useful information
REPO=$(git config remote.origin.url)
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=$(git rev-parse --verify HEAD)

# Clone the existing gh-pages for this repo into out/
# Create a new empty branch if gh-pages doesn't exist yet (should only happen on first deploy)
git clone $REPO "${build_dir}"
pushd "${build_dir}"
git checkout $TARGET_BRANCH || git checkout --orphan $TARGET_BRANCH
popd

# Clean out existing contents
rm -rf "${build_dir}"/**/* || exit 0

# Run our compile script
doCompile "${build_dir}"

# Now let's go have some fun with the cloned repo
cd "${build_dir}"
git config user.name "Travis CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"

# If there are no changes to the compiled out (e.g. this is a README update) then just bail.
git diff --quiet && {
    echo "No changes to the output on this push; exiting."
    exit 0
}

# Commit the "changes", i.e. the new version.
# The delta will show diffs between new and old versions.
git add --all .
git commit -m "Deploy to GitHub Pages: ${SHA}"

# Add the deploy key to the ssh agent for git commits
chmod 600 .private/deploy_key
eval `ssh-agent -s`
ssh-add deploy_key

# Now that we're all set up, we can push.
git push $SSH_REPO $TARGET_BRANCH
