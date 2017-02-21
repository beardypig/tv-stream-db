#!/bin/bash
set -e # Exit with nonzero exit code if anything fails

function log {
    echo "[$(date --rfc-3339=seconds)]: $*" >&2
}

dist_dir=${1:-.dist}
mkdir -p "${dist_dir}"

log "Compiling site template..."
python src/build_listing_html.py "src/templates/" "datafiles/streams/" "${dist_dir}"

log "Copying static files..."
cp -r src/static/* "${dist_dir}/"
