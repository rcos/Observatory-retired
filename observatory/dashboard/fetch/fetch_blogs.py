#!/usr/bin/env python

# Copyright (c) 2010, individual contributors (see AUTHORS file)
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

# Blog fetching is pretty much always fast, so it does not need to be broken
# up into multiple processes. This script should just be run in cron.

import os, subprocess
from fetch_core import setup_environment, cprint
from Queue import Queue
from threading import Thread
from time import sleep
from sys import executable as python

setup_environment()

from dashboard.models import Blog, Project
from observatory.settings import BLOG_FETCH_PROCESS_COUNT

this_dir = os.path.abspath(os.path.dirname(__file__))
fetch_script = os.path.join(this_dir, "fetch_single_blog.py")

class Fetcher(object):
  def __init__(self, blog):
    self.blog = blog
    self.process = subprocess.Popen([python, fetch_script, str(blog.id), "&"])
  
  def is_done(self):
    self.process.poll()
    return self.process.returncode is not None

blogs = list(Blog.objects.filter(from_feed = True))
fetchers = []

while True:
  if len(blogs) is 0 and len(fetchers) is 0:
    break
  
  while len(fetchers) < BLOG_FETCH_PROCESS_COUNT and len(blogs) > 0:
    fetchers.append(Fetcher(blogs.pop()))
  
  sleep(1)
  
  for fetcher in fetchers:
    if fetcher.is_done():
      # if the blog is not a personal blog, update the project's score
      if fetcher.blog.user is None:
        project = Project.objects.get(blog__id = fetcher.blog.id)
        project.calculate_score()
      
      # remove the fetcher
      fetchers.remove(fetcher)

