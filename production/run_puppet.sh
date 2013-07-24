#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$DIR/.."
librarian-puppet install

puppet apply  --modulepath "$DIR/../modules" $DIR/../puppet/base.pp --detailed-exitcodes || [ $? -eq 2 ]
