#!/usr/bin/env python

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

# Blog fetching is pretty much always fast, so it does not need to be broken
# up into multiple processes. This script should just be run in cron.

from fetch_core import setup_environment, cprint
from Queue import Queue
from threading import Thread

setup_environment()

from dashboard.models import Blog, Project
from observatory.settings import BLOG_FETCH_THREAD_COUNT

if BLOG_FETCH_THREAD_COUNT > 1:
  def fetcher():
    while True:
      try:
        # get the next blog
        blog = queue.get()
        
        # don't fetch internally hosted blogs
        if blog.from_feed:
          title = blog.project.title        
          cprint("==> Fetching the blog for {0}".format(title),
                 "magenta", attrs=["bold"])
          blog.fetch()
          cprint("==> Done fetching the blog for {0}".format(title),
                 "green", attrs=["bold"])
        
        # all done!
        queue.task_done()
      except:
        queue.task_done()
        raise

  # build a queue
  queue = Queue()
  for blog in Blog.objects.all():
    queue.put(blog)

  # run the threads
  for i in range(BLOG_FETCH_THREAD_COUNT):
    thread = Thread(target = fetcher)
    thread.daemon = True
    thread.start()

  # wait until we're finished
  queue.join()
else:
  for blog in Blog.objects.all():
    if blog.from_feed:
      title = blog.project.title        
      cprint("==> Fetching the blog for {0}".format(title),
             "magenta", attrs=["bold"])
      blog.fetch()
      cprint("==> Done fetching the blog for {0}".format(title),
             "green", attrs=["bold"])
      
      project = Project.objects.get(blog__id = blog.id)
      project.calculate_score()
