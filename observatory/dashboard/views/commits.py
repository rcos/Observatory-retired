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

from dashboard.models import Commit
from dashboard.util import url_pathify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from lib.markdown import markdown

def show(request, project_url_path, commit_url_path):
  # redirect to the properly formatted path if needed
  project_url = url_pathify(project_url_path)
  commit_url = url_pathify(commit_url_path)
  if project_url != project_url_path or commit_url != commit_url_path:
    return HttpResponseRedirect(reverse('dashboard.views.commits.show',
                                        args = (project_url, commit_url)))
  
  # find the commit
  commit = get_object_or_404(Commit, url_path = commit_url)
  
  # if the commit is external, redirect to it
  if commit.repository.from_feed:
    return HttpResponseRedirect(commit.url)
  
  return render_to_response("commits/show.html", {
      'commit': commit
    }, context_instance = RequestContext(request))