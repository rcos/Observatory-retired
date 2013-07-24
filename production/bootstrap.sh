#!/bin/bash

set -e

ssh deploy@$1 "
sudo apt-get -y install git
git clone git://github.com/rcos/Observatory.git -b master --recursive
sudo ~/Observatory/production/setup_puppet.sh
sudo ~/Observatory/production/run_puppet.sh
"
