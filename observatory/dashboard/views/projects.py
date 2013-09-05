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
from colorsys import hsv_to_rgb
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from dashboard.models import *
from dashboard.forms import *
from dashboard.util import ListPaginator, url_pathify, force_url_paths

SHOW_COMMIT_COUNT = 5
SHOW_BLOGPOST_COUNT = 3

# the classic "dashboard" view, with rankings
def list(request):
  projects = Project.objects.exclude(active = False).exclude(score = None).exclude(pending= True).order_by('score')
  scoreless = Project.objects.filter(score = None).exclude(active = False).exclude(pending= True)
  
  # fetch repositories and blogs in single queries
  repositories = Repository.objects.exclude(project = None)
  blogs = Blog.objects.exclude(project = None)
  
  repository_dict = {}
  blogs_dict = {}
  
  for repository in repositories:
    repository_dict[repository.id] = repository
  for blog in blogs:
    blogs_dict[blog.id] = blog



  # assign the repositories and blogs
  for project in projects:
    project.repository = repository_dict[project.repository_id]
    project.blog = blogs_dict[project.blog_id]
  
  # find the number of updates for blog, repo and overall in the past week
  repo_count, blog_count, overall_count = 0, 0, 0
  now = datetime.utcnow()
  for project in projects:
    repo_days = (now - project.repository.most_recent_date).days
    blog_days = (now - project.blog.most_recent_date).days
    if repo_days < 7: repo_count += 1
    if blog_days < 7: blog_count += 1
    if repo_days < 7 or blog_days < 7: overall_count += 1
  
  # create CSS for the progress bars at the top
  def css(count):
    grad_top = hsv_to_rgb(0.3 * count / projects.count(), 0.9, 0.5)
    grad_bottom = hsv_to_rgb(0.3 * count / projects.count(), 0.9, 0.9)
    border = hsv_to_rgb(0.3 * count / projects.count(), 0.9, 0.7)
    
    return """
      background:rgb({3},{4},{5});
      background-image: -webkit-gradient(linear, left bottom, left top,
        from(rgb({0},{1},{2})),
        to(rgb({3},{4},{5})));
      background-image: -moz-linear-gradient(100% 100% 90deg,
        rgb({0},{1},{2}),
        rgb({3},{4},{5})
      );
      border: 1px solid rgb({6},{7},{8});
      width:{9}px;display: block;""".format(
        int(grad_top[0] * 255),
        int(grad_top[1] * 255),
        int(grad_top[2] * 255),
        int(grad_bottom[0] * 255),
        int(grad_bottom[1] * 255),
        int(grad_bottom[2] * 255),
        int(border[0] * 255),
        int(border[1] * 255),
        int(border[2] * 255),
        int(424 * (1.0 * count / projects.count()))
      )
      
  if projects.count() != 0:
    repo_bar_css = css(repo_count)
    blog_bar_css = css(blog_count)
    overall_bar_css = css(overall_count)
  else:
    repo_bar_css, blog_bar_css, overall_bar_css = None, None, None
  
  return render_to_response('projects/list.html', {
      'projects': projects,
      'scoreless': scoreless,
      'blog_count': blog_count,
      'repo_count': repo_count,
      'overall_count': overall_count,
      'repo_bar_css': repo_bar_css,
      'blog_bar_css': blog_bar_css,
      'overall_bar_css': overall_bar_css,
      'nothing_fetched': projects.count() is 0
    }, context_instance = RequestContext(request))

# "dashboard" view for archived projects without scoring
def archived_list(request):
  projects = Project.objects.exclude(score = None).exclude(active = True).exclude(pending= True).order_by('score')
  scoreless = Project.objects.filter(score = None).exclude(active = True).exclude(pending= True)


  
  # fetch repositories and blogs in single queries
  repositories = Repository.objects.exclude(project = None)
  blogs = Blog.objects.exclude(project = None)
  
  repository_dict = {}
  blogs_dict = {}
  
  for repository in repositories:
    repository_dict[repository.id] = repository
  for blog in blogs:
    blogs_dict[blog.id] = blog



  # assign the repositories and blogs
  for project in projects:
    project.repository = repository_dict[project.repository_id]
    project.blog = blogs_dict[project.blog_id]
  
  # find the number of updates for blog, repo and overall in the past week
  repo_count, blog_count, overall_count = 0, 0, 0
  now = datetime.utcnow()
  for project in projects:
    repo_days = (now - project.repository.most_recent_date).days
    blog_days = (now - project.blog.most_recent_date).days
    if repo_days < 7: repo_count += 1
    if blog_days < 7: blog_count += 1
    if repo_days < 7 or blog_days < 7: overall_count += 1
  
  
  return render_to_response('projects/archive_list.html', {
      'projects': projects,
      'scoreless': scoreless,
      'blog_count': blog_count,
      'repo_count': repo_count,
      'nothing_fetched': projects.count() is 0
    }, context_instance = RequestContext(request))

# "dashboard" view for archived projects without scoring
def pending_list(request):
  projects = Project.objects.filter(pending= True)
  
  return render_to_response('projects/pending_list.html', {
      'projects': projects,
      'nothing_fetched': projects.count() is 0
    }, context_instance = RequestContext(request))

def add_mentor(request):
  mentor = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))

  if not mentor.info.mentor:
    return HttpResponseRedirect(reverse(show, args=(project.url_path)))

  if int(request.user.id) != mentor.id:
    return HttpResponseRedirect(reverse(show, args=(project.url_path)))

  project.mentor = mentor
  project.save()

  return HttpResponseRedirect(reverse(show, args = (project.url_path,)))

def approve(request, project_url_path):
  try:
    mentor = request.user.info.mentor
  except:
    mentor = False
  project = get_object_or_404(Project, url_path = project_url_path)
  if project.mentor and mentor:
    project.pending = False
    project.save()
  return pending_list(request)

def deny(request, project_url_path):
  try:
    mentor = request.user.info.mentor
  except:
    mentor = False
  if mentor:
    project = get_object_or_404(Project, url_path = project_url_path)
    project.delete()
  return pending_list(request)

# information about a specific project
def show(request, project_url_path):
  # redirect if the url path is not in the correct format
  resp = force_url_paths('dashboard.views.projects.show', project_url_path)
  if resp: return resp
  
  # get the project
  project = get_object_or_404(Project, url_path = project_url_path)


  
  # create a paginated list of the screenshots of the project
  paginator = None
  screenshots = Screenshot.objects.filter(project = project)
  if screenshots.count > 0:
    paginator = ListPaginator(screenshots.order_by('id').reverse(), 3)
  
  # get the most recent commits for the project
  commits = Commit.objects.filter(repository = project.repository)
  commits = commits.order_by('date').reverse()[:SHOW_COMMIT_COUNT]
  
  # get the project's contributors
  contributors = Contributor.objects.filter(projects__id__exact = project.id)
  
  # exclude the current authors from the project
  for user in project.authors.all():
    contributors = contributors.exclude(user = user)

  # if the user has already submitted an author request, hide add/remove author
  show_add_remove_author = True
  if request.user is not None:
    try:
      AuthorRequest.objects.get(project = project, user = request.user)
      show_add_remove_author = False
    except:
      pass
  
  # get the most recent blog posts for the project
  blogposts = BlogPost.objects.filter(blog = project.blog)
  blogposts = blogposts.order_by('date').reverse()[:SHOW_BLOGPOST_COUNT]
  return render_to_response('projects/show.html', {
      'project': project,
      'paginator': paginator,
      'authors': project.authors.all(),
      'default_page': 1,
      'has_screenshots': len(screenshots) > 0,
      'screenshot_pages_width': len(screenshots) * 790,
      'js_page_id': 'show_project',
      'blogposts': blogposts,
      'commits': commits,
      'contributors': contributors,
      'show_add_remove_author': show_add_remove_author,
      'mentor': project.mentor,
    }, context_instance = RequestContext(request))

# a view for adding a new project
@login_required
def add(request):
  feed_repo_form = FeedRepositoryForm()
  cloned_repo_form = ClonedRepositoryForm()
  project_form = ProjectForm()
  blog_form = BlogForm()
  
  form_keys = {
    1: ('title', 'description', 'website', 'wiki'),
    2: ('web_url', 'clone_url', 'vcs', 'repo_rss', 'cmd'),
    3: ('url', 'rss')
  }
  
  if 'current' in request.POST:
    current = int(request.POST['current'])
  else:
    current = 0
  
  if current == 1:
    project_form = ProjectForm(request.POST)
    if not project_form.is_valid():
      current -= 1
  
  elif current == 2:
    if 'clone_url' in request.POST:
      cloned_repo_form = ClonedRepositoryForm(request.POST)
      if not cloned_repo_form.is_valid():
        current -= 1
    elif 'repo_rss' in request.POST:
      feed_repo_form = FeedRepositoryForm(request.POST)
      if not feed_repo_form.is_valid():
        current -= 1
  
  elif current == 3:
    blog_form = BlogForm(request.POST)
    if not ('url' not in request.POST or blog_form.is_valid()):
      current -= 1
  
  # go to the next form
  current += 1
  
  # if there are more parts to the form
  if current < 4:
    # remove the csrf token and current from a copy of the POST data
    post = request.POST.copy()
    if 'csrfmiddlewaretoken' in post:
      post.pop('csrfmiddlewaretoken')
      post.pop('current')

      # remove any of the keys that should be set on this form page
      for key in form_keys[current]:
        try:
          post.pop(key)
        except:
          pass
    
    return render_to_response('projects/add.html', {
        'parts': [1, 2, 3],
        'current': current,
        'previous_data': post,
        'cloned_repo_form': cloned_repo_form,
        'feed_repo_form': feed_repo_form,
        'project_form': project_form,
        'blog_form': blog_form,
        'js_page_id': 'add_project'
      }, context_instance = RequestContext(request))
  
  # otherwise, if the form is complete, create the project
  else:
    # validate and clean all forms
    project_form = ProjectForm(request.POST)
    cloned_repo_form = ClonedRepositoryForm(request.POST)
    feed_repo_form = FeedRepositoryForm(request.POST)
    blog_form = BlogForm(request.POST)
    
    for form in [project_form, cloned_repo_form, feed_repo_form, blog_form]:
      form.is_valid()
    
    # create the blog object
    if 'rss' in request.POST:
      blog = Blog(url = blog_form.cleaned_data['url'],
                  rss = blog_form.cleaned_data['rss'],
                  from_feed = True)
    else:
      blog = Blog(from_feed = False)
    blog.save()

    # create the repository object
    # if using google code removes read only addition
    # if git@ is mistakenly typed, git:// is placed in
    if 'clone_url' in request.POST:
      url = cloned_repo_form.cleaned_data['clone_url']
      gitfix = url.replace('git@', 'git://')
      url = gitfix
      if "google.com" in url:
        split = url.split(' ')
        url = split[0]

      repo = Repository(web_url = cloned_repo_form.cleaned_data['web_url'],
                        clone_url = url,
                        from_feed = False)
    else:
      repo = Repository(web_url = feed_repo_form.cleaned_data['web_url'],
                        repo_rss = feed_repo_form.cleaned_data['repo_rss'],
                        from_feed = True)
    repo.save()

    # create the project object
    project = Project(title = project_form.cleaned_data['title'],
                      website = project_form.cleaned_data['website'],
                      wiki = project_form.cleaned_data['wiki'],
                      description = project_form.cleaned_data['description'],
                      active = True,
                      repository_id = repo.id,
                      blog_id = blog.id,
					  pending = True)

    # get the project a primary key
    project.save()

    # associate the current user with the project as an author
    project.authors.add(request.user)

    # save the project again
    project.save()

    # Set the active flag as true
    project.active = True

    # Save the project again
    project.save()

    # redirect to the show page for the new project
    return HttpResponseRedirect(reverse(show, args = (project.url_path,)))

# a view for modifying an existing project
@login_required
def modify(request, project_url_path, tab_id = 1):
  # redirect if the url path is not in the correct format
  resp = force_url_paths(modify, project_url_path)
  if resp: return resp
  
  project = get_object_or_404(Project, url_path = project_url_path)
  screenshots = Screenshot.objects.filter(project = project)
  
  # if someone tries to edit a project they shouldn't be able to
  if not (request.user in project.authors.all() or request.user.info.mentor):
    return HttpResponseRedirect(reverse(show, args = (project.url_path,)))
  
  # default forms
  project_form = ProjectForm(instance = project)
  cloned_repo_form = ClonedRepositoryForm(instance = project.repository)
  feed_repo_form = FeedRepositoryForm(instance = project.repository)
  blog_form = BlogForm(instance = project.blog)
  screenshot_form = UploadScreenshotForm()
  
  # if changes should be saved or rejected
  if request.POST:
    # uploading a screenshot
    if 'screenshot_upload' in request.POST:
      form = UploadScreenshotForm(request.POST, request.FILES)
      if form.is_valid():
        Screenshot.create(form, request.FILES["file"], project)
      else:
        screenshot_form = form

    # wrote a post with the js overlay
    if 'title' in request.POST and 'markdown' in request.POST:
      from dashboard.views.blogs import create_post_real
      return create_post_real(request.POST)

    # editing the project's information
    elif 'title' in request.POST:
      form = ProjectForm(request.POST)
      
      # if the form is valid, save
      if form.is_valid():
        project.title = form.cleaned_data['title']
        project.website = form.cleaned_data['website']
        project.wiki = form.cleaned_data['wiki']
        project.description = form.cleaned_data['description']
        project.active = form.cleaned_data['active']
        project.save()
        project_form = ProjectForm(instance = project)
      
      # otherwise, display the errors
      else:
        project_form = form
    
    # editing a cloned repository
    elif 'clone_url' in request.POST:
      form = ClonedRepositoryForm(request.POST)
      
      if form.is_valid():
        project.repository.web_url = form.cleaned_data['web_url']
        project.repository.clone_url = form.cleaned_data['clone_url']
        project.repository.vcs = form.cleaned_data['vcs']
        project.repository.from_feed = False
        project.repository.save()
        cloned_repo_form = ClonedRepositoryForm(instance = project.repository)
      else:
        cloned_repo_form = form
    
    # editing a feed repository
    elif 'repo_rss' in request.POST:
      form = FeedRepositoryForm(request.POST)
      
      if form.is_valid():
        project.repository.repo_rss = form.cleaned_data['repo_rss']
        project.repository.cmd = form.cleaned_data['cmd']
        project.repository.web_url = form.cleaned_data['web_url']
        project.repository.from_feed = True
        project.repository.save()
        feed_repo_form = FeedRepositoryForm(instance = project.repository)
      else:
        feed_repo_form = form
    
    # editing a feed-based blog
    elif 'url' in request.POST:
      form = BlogForm(request.POST)
      
      if form.is_valid():
        project.blog.url = form.cleaned_data['url']
        project.blog.rss = form.cleaned_data['rss']
        project.blog.from_feed = True
        project.blog.save()
        blog_form = BlogForm(instance = project.blog)
      else:
        blog_form = form
    
    # switching to hosted blog
    elif 'switch-to-hosted' in request.POST:
      project.blog.from_feed = False
      project.blog.save()
      
  return render_to_response('projects/modify.html', {
    'project': project,
    'screenshots': screenshots,
    'project_form': project_form,
    'cloned_repo_form': cloned_repo_form,
    'feed_repo_form': feed_repo_form,
    'blog_form': blog_form,
    'screenshot_form': screenshot_form,
    'post_form': BlogPostForm(),
    'repo': project.repository,
    'tab': int(tab_id)
  }, context_instance = RequestContext(request))


	

# adds a user as an author of a project
def add_user(request):
  # get the user and project
  user = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))
  
  # don't let people add other users
  if int(request.user.id) != user.id:
    import logging
    logger = logging.getLogger('django.debug')
    logger.warning('%s != %s for request %s' % (request.user.id, user.id, request))
    return HttpResponseRedirect(reverse(show, args = (project.url_path,)))
  
  # find the current authors of the project
  authors = project.authors.all()
  
  # if the user is not already an author of the project
  if user not in authors:
    # if there are no authors, allow the user to "claim" the project
    if len(authors) == 0:
      project.authors.add(user)
      project.save()
  
    # otherwise, send a request to all of the current authors
    else:
      request = AuthorRequest(user_id = user.id, project_id = project.id)
      request.save()
  
  # redirect back to the show page
  return HttpResponseRedirect(reverse(show, args = (project.url_path,)))

# removes a user as an author of a project
def remove_user(request):
  # get the user and project
  user = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))
  
  # don't let people delete other users
  if request.user.id != user.id:
    return HttpResponseRedirect(reverse(show, args = (project.url_path,)))
  
  # removes the user from the project
  if user in project.authors.all():
    project.authors.remove(user)
  
  # save
  project.save()
  
  # redirect back to the show page
  return HttpResponseRedirect(reverse(show, args = (project.url_path,)))

@login_required
def delete_screenshot(request, project_url_path, screenshot_id):
  project = get_object_or_404(Project, url_path = project_url_path)
  
  if request.user not in project.authors.all():
    return HttpResponseRedirect(reverse(show, args = (project.url_path,)))
  
  screenshot = get_object_or_404(Screenshot, id = screenshot_id)
  screenshot.delete()
  
  return HttpResponseRedirect(reverse(modify, args = (project.url_path, 4)))
