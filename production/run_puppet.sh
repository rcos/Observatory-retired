#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

puppet apply  --modulepath "$DIR/../modules" $DIR/../puppet/base.pp --detailed-exitcodes || [ $? -eq 2 ]
