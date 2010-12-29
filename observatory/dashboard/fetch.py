#! /usr/bin/env python

# Copyright (c) 2010, Nate Stedman <natesm@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# this is the fetch script for observatory.
# it should be run in cron or manually.

import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
sys.path.insert(0, os.path.abspath(os.path.join(path, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(path, '..', '..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'observatory.settings'

from dashboard.models import *

# fetch the projects and calculate their scores
for project in Project.objects.all():
  project.fetch()

# rank the projects
rank = 1
for project in Project.objects.order_by('score').reverse():
  project.rank = rank
  project.save()
  rank += 1