#!/bin/bash

set -e

ssh deploy@$1 "
apt-get -y install git
git clone git://github.com/rcos/Observatory.git -b master --recursive
~/Observatory/production/setup_puppet.sh
~/Observatory/production/run_puppet.sh
"
