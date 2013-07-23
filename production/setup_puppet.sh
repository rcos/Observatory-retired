#!/bin/bash

set -e

cd /tmp
wget http://apt.puppetlabs.com/puppetlabs-release-precise.deb
dpkg -i puppetlabs-release-precise.deb
rm puppetlabs-release-precise.deb
apt-key adv --recv-key --keyserver pool.sks-keyservers.net 4BD6EC30
apt-get update
apt-get install puppet -y
