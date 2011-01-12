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

from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from dashboard.models import *
from lib.InheritanceQuerySet import InheritanceQuerySet

from django.db import connection

INDEX_EVENT_COUNT = 4

# the main page for dashboard, a feed showing recent Events
def index(request):
  qs = InheritanceQuerySet(model = Event)
  objs = qs.select_subclasses().order_by('date').reverse()[:INDEX_EVENT_COUNT]
  
  projects = {}
  authors = {}
  for event in objs:
    if event.project_id not in projects:
      projects[event.project_id] = event.project
    if event.author_id not in authors:
      authors[event.author_id] = event.author
  
  return render_to_response('main/index.html', {
      'events': objs,
      'authors': authors,
      'projects': projects
    }, context_instance = RequestContext(request))