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
from threading import Thread
from Queue import Queue

# set django's required paths
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)
sys.path.insert(0, os.path.abspath(os.path.join(path, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(path, '..', '..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'observatory.settings'

# now we can import from observatory's stuff
from dashboard.models import Project
from observatory.settings import FETCH_THREAD_COUNT

if FETCH_THREAD_COUNT > 1:
  def fetcher():
    while True:
      try:
        project = queue.get()
        project.fetch()
        queue.task_done()
      except:
        queue.task_done()
        raise

  # build a queue
  queue = Queue()
  for project in Project.objects.all():
    queue.put(project)

  # run the threads
  for i in range(FETCH_THREAD_COUNT):
    thread = Thread(target = fetcher)
    thread.daemon = True
    thread.start()

  # wait until we're finished
  queue.join()
else:
  for project in Project.objects.all():
    print "Fetching {0}".format(project.title)
    project.fetch()

# rank the projects
rank = 1
for project in Project.objects.order_by('score'):
  project.rank = rank
  project.save()
  rank += 1
