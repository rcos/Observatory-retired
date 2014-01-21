#!/usr/bin/env python

import os
import os.path
import sys

if __name__ == "__main__":

    #Include parent directory in the path by default
    path = os.path.abspath('../')
    if path not in sys.path:
        sys.path.append(path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observatory.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
