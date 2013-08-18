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

from dashboard.models import Commit, Project
from dashboard.util import force_url_paths, avoid_duplicate_queries
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from markdown import markdown

COMMITS_PER_PAGE = 30

def all(request):
  return all_page(request, 1)

def all_page(request, page_num):
  return show_page(request, page_num,
                   Commit.objects.order_by('-date'),
                   "commits/show_all.html")

def show_user(request, user_id):
  pass

def show_repository(request, project_url_path):
  resp = force_url_paths(show_repository, project_url_path)
  if resp: return resp
  
  return repository_page(request, project_url_path, 1)

def repository_page(request, project_url_path, page_num):
  resp = force_url_paths(repository_page, project_url_path, page = page_num)
  if resp: return resp
  
  project = get_object_or_404(Project, url_path = project_url_path)
  
  qs = Commit.objects.order_by('-date').filter(project = project)
  return show_page(request, page_num, qs,
                   'commits/show_repository.html',
                   project = project)

def show_page(request, page_num, queryset, template, project = None):
  paginator = Paginator(queryset, COMMITS_PER_PAGE)
  
  # if the page requested does not exist, 404
  if int(page_num) not in paginator.page_range:
    raise Http404
  
  page = paginator.page(page_num)
  avoid_duplicate_queries(page.object_list, "author", "project",
                          author = { request.user.id: request.user }
                                   if request.user.is_authenticated() else {},
                          project = { project.id: project }
                                    if project is not None else {})
  
  # otherwise, render
  return render_to_response(template, {
      'page': page,
      'disable_content': True,
      'project': project
    }, context_instance = RequestContext(request))

def show(request, project_url_path, commit_url_path):
  resp = force_url_paths(show, project_url_path, commit_url_path)
  if resp: return resp
  
  # find the commit
  commit = get_object_or_404(Commit, url_path = commit_url_path)
  
  # if the commit is external, redirect to it
  if commit.repository.from_feed and commit.url:
    return HttpResponseRedirect(commit.url)
  
  return render_to_response("commits/show.html", {
      'commit': commit
    }, context_instance = RequestContext(request))
