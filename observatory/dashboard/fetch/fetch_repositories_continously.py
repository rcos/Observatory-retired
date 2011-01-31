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

FETCH_EVERY_SECONDS = 5 * 60

import datetime, os, subprocess
from sys import executable as python
from time import time, sleep

this_dir = os.path.abspath(os.path.dirname(__file__))
fetch_script = os.path.join(this_dir, "fetch_repositories.py")

while True:
  start_time = time()
  
  process = subprocess.Popen([python, fetch_script])
  process.wait()
  
  delta = time() - start_time
  
  if delta < FETCH_EVERY_SECONDS:
    print "Waiting for {0} seconds".format(FETCH_EVERY_SECONDS - delta)
    sleep(FETCH_EVERY_SECONDS - delta)
  else:
    print "That took a while, restarting immediately..."
