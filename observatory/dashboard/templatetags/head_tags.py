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

from django import template
from django.template.loader import render_to_string
from observatory.settings import DEBUG

register = template.Library()

CSS_FILES=[
  "css/author-requests.css",
  "css/base.css",
  "css/basics.css",
  "css/buttons.css",
  "css/decorations.css",
  "css/diffs.css",
  "css/events.css",
  "css/forms.css",
  "css/modify.css",
  "css/profiles.css",
  "css/projects.css",
  "css/rcos.css"
]

JS_FILES=[
  "js/lib/vendor/jquery-1.4.4.js",
  "js/lib/vendor/jquery.html5form-1.2-min.js",
  "js/lib/vendor/jquery.lightbox-0.5.min.js",
  "js/globals.js",
  
  # forms
  "js/lib/form/Form.js",
  "js/lib/form/ExclusiveOrForms.js",
  
  # pages
  "js/lib/page/Page.js",
  "js/lib/page/LoginRegisterPage.js",
  "js/lib/page/AddProjectPage.js",
  "js/lib/page/ShowProjectPage.js",
  "js/lib/page/ModifyProjectPage.js",
  
  "js/init.js"
]

CSS_LINK = "<link rel='stylesheet' type='text/css' href='/site-media/{0}' />"
JS_LINK = "<script src='/site-media/{0}'></script>"

def head_tags():
  if DEBUG:
    return ("".join([CSS_LINK.format(file) for file in CSS_FILES]) + 
            "".join([JS_LINK.format(file) for file in JS_FILES]))
  else:
    return (CSS_LINK.format("style.css") +
            "".join([JS_LINK.format(file) for file in JS_FILES]))

register.simple_tag(head_tags)
