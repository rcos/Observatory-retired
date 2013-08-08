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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from dashboard.models import *
from dashboard.util import force_url_paths, avoid_duplicate_queries
from dashboard.views import commits, blogs

from django.db import connection

INDEX_EVENT_COUNT = 100

# a feed showing recent Events
def feed(request):
  objs = Event.objects.select_subclasses().order_by('date').reverse()[:INDEX_EVENT_COUNT]
  
  avoid_duplicate_queries(objs, "author", "project",
                          author = { request.user.id: request.user }
                                   if request.user.is_authenticated() else {})
  
  return render_to_response('feed/feed.html', {
      'events': objs,
      'disable_content': True
    }, context_instance = RequestContext(request))

# a URL that will redirect to the specific page for a type of event
def event(request, url_path):
  resp = force_url_paths(event, url_path)
  if resp: return resp
  
  try:
    qs = InheritanceQuerySet(model = Event)
    the_event = qs.select_subclasses().get(url_path = url_path)
  except:
    raise Http404
  
  if the_event.__class__ is Commit:
    return HttpResponseRedirect(reverse(commits.show,
                                        args = (the_event.project.url_path,
                                                the_event.url_path,)))
  else:
    if the_event.project is not None:
      return HttpResponseRedirect(reverse(blogs.show_post,
                                          args = (the_event.project.url_path,
                                                  the_event.url_path,)))
    else:
      return HttpResponseRedirect(reverse(blogs.show_user_post,
                                          args = (the_event.author.id,
                                                  the_event.url_path,)))
  raise Http404
