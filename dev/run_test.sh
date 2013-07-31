#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$DIR/../:$DIR/../observatory"
export DJANGO_SETTINGS_MODULE="observatory.settings"
py.test "$DIR/../observatory"

