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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from dashboard.models import *
from lib.InheritanceQuerySet import InheritanceQuerySet

from django.db import connection

INDEX_EVENT_COUNT = 100

# the main page for dashboard, a feed showing recent Events
def index(request):
  qs = InheritanceQuerySet(model = Event)
  objs = qs.select_subclasses().order_by('date').reverse()[:INDEX_EVENT_COUNT]
  
  events = []
  projects = {}
  authors = { request.user.id: request.user } if request.user else {}
  
  for obj in objs:
    event = { 'event': obj }
    
    if obj.author_id is not None:
      if obj.author_id not in authors:
        authors[obj.author_id] = User.objects.get(id = obj.author_id)
      event['author'] = authors[obj.author_id]
    
    if obj.project_id is not None:
      if obj.project_id not in projects:
        projects[obj.project_id] = Project.objects.get(id = obj.project_id)
      event['project'] = projects[obj.project_id]
    
    events.append(event)
  
  return render_to_response('main/index.html', {
      'events': events
    }, context_instance = RequestContext(request))