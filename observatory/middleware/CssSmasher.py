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

import os
import re
from django.core.exceptions import MiddlewareNotUsed
from observatory.settings import MEDIA_ROOT, JS_FILES, CSS_FILES

class CssSmasher(object):
  def __init__(self):
    cssdir = os.path.join(MEDIA_ROOT, 'css')
    with open(os.path.join(MEDIA_ROOT, 'style.css'), 'w') as stylecss:
      for file in os.listdir(cssdir):
        with open(os.path.join(cssdir, file), 'r') as cssfile:
          stylecss.write(re.sub(r"\s+", ' ', cssfile.read()))
    
    with open(os.path.join(MEDIA_ROOT, "observatory.js"), 'w') as js:
      for jsfile in [os.path.join(MEDIA_ROOT, path) for path in JS_FILES]:
        with open(jsfile, "r") as jsdata:
          js.write(re.sub(r"\s+", " ", jsdata.read()))

    raise MiddlewareNotUsed
