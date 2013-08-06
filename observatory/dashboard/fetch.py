#! /usr/bin/env python2

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

# This script shouldn't be used in production, it's just a shortcut for quick
# use with demo.py. Realistically, blogs don't need to be fetched nearly as
# often as repositories, and github can take the hits a lot better than
# peoples personal servers can. Just don't DOS anyone.

import os, subprocess
from sys import executable as python

this_dir = os.path.abspath(os.path.dirname(__file__))
blogs_script = os.path.join(this_dir, "fetch", "fetch_blogs.py")
repos_script = os.path.join(this_dir, "fetch", "fetch_repositories.py")
warning_script = os.path.join(this_dir, "fetch", "fetch_warnings.py")

blogs = subprocess.Popen([python, blogs_script])
repos = subprocess.Popen([python, repos_script])
warnings= subprocess.Popen([python, warning_script])

blogs.wait()
repos.wait()
warnings.wait()
