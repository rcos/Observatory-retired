#!/bin/bash

set -e

git push origin $(git tag -l v\* | sort -V | tail -1)
ssh -t deploy@$1 "
cd /home/deploy/Observatory
git checkout master
git pull origin
git fetch --tags
git checkout $(git tag -l v\* | sort -V | tail -1)
sudo /home/deploy/Observatory/production/run_puppet.sh
"
