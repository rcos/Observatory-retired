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

from dashboard.models import Project
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
  projects = Project.objects.filter(active = True).order_by("score")
  i = 0
  for project in projects:
	if (project.random_main_page_screenshot() is not None):
		i = i + 1
	else:
		ptitle = project.title
		projects = projects.exclude(title = ptitle)
	if (i == 3):
	    projects = projects [:3]
	    break


  return render_to_response('foundry/index.html', {
      'disable_content': True,
      'projects': projects
    }, context_instance = RequestContext(request))


def mokr(request):
  return render_to_response('foundry/mokr_resources.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))








