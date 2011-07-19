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

import os, subprocess
from fetch_core import setup_environment, cprint
from sys import argv

setup_environment()

from dashboard.models import Blog, Project
from observatory.settings import BLOG_FETCH_PROCESS_COUNT

blog = Blog.objects.get(id = argv[1])

if blog.from_feed:
  try:
    title = blog.project.title
  except:
    try:
		title = blog.user.get_full_name()
    except:
		title = "Unknown"
  cprint("==> Fetching the blog for {0}".format(title), "magenta", attrs=["bold"])
  blog.fetch()
  cprint("==> Done fetching the blog for {0}".format(title), "green", attrs=["bold"])


