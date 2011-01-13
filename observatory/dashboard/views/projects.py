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

import Image
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
from settings import SCREENSHOT_PATH

SHOW_COMMIT_COUNT = 5
SHOW_BLOGPOST_COUNT = 3

# the classic "dashboard" view, with rankings
def list(request):
  projects = Project.objects.exclude(score = None).order_by('score')
  scoreless = Project.objects.filter(score = None)
  
  # find the number of updates for blog, repo and overall in the past week
  repo_count, blog_count, overall_count = 0, 0, 0
  now = datetime.utcnow()
  for project in projects:
    repo_days = (now - project.repository.most_recent_date).days
    blog_days = (now - project.blog.most_recent_date).days
    if repo_days < 7: repo_count += 1
    if blog_days < 7: blog_count += 1
    if repo_days < 7 or blog_days < 7: overall_count += 1
  
  print blog_count, repo_count, overall_count
  
  # create CSS for the progress bars at the top
  def css(count):
    grad_top = hsv_to_rgb(0.3 * count / projects.count(), 0.9, 0.5)
    grad_bottom = hsv_to_rgb(0.3 * count / projects.count(), 0.9, 0.9)
    border = hsv_to_rgb(0.3 * count / projects.count(), 0.9, 0.7)
    
    print count, projects.count(), int(100 * (1.0 * count / projects.count()))
    
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
      
  if projects.count() is not 0:
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
      'js_page_id': 'show_project',
      'blogposts': blogposts,
      'commits': commits,
      'show_add_remove_author': show_add_remove_author
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
    if 'clone_url' in request.POST:
      repo = Repository(web_url = cloned_repo_form.cleaned_data['web_url'],
                        clone_url = cloned_repo_form.cleaned_data['clone_url'],
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
                      blog_id = blog.id)

    # get the project a primary key
    project.save()

    # associate the current user with the project as an author
    project.authors.add(request.user)

    # save the project again
    project.save()

    # redirect to the show page for the new project
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.url_path,)))

# a view for modifying an existing project
@login_required
def modify(request, project_url_path, tab_id = 1):
  # redirect if the url path is not in the correct format
  resp = force_url_paths('dashboard.views.projects.modify', project_url_path)
  if resp: return resp
  
  project = get_object_or_404(Project, url_path = project_url_path)
  
  # if someone tries to edit a project they shouldn't be able to
  if request.user not in project.authors.all():
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.url_path,)))
  # default forms
  project_form = ProjectForm(instance = project)
  cloned_repo_form = ClonedRepositoryForm(instance = project.repository)
  feed_repo_form = FeedRepositoryForm(instance = project.repository)
  blog_form = BlogForm(instance = project.blog)
  
  # if changes should be saved or rejected
  if request.POST:
    # editing the project's information
    if 'title' in request.POST:
      form = ProjectForm(request.POST)
      
      # if the form is valid, save
      if form.is_valid():
        project.title = form.cleaned_data['title']
        project.website = form.cleaned_data['website']
        project.wiki = form.cleaned_data['wiki']
        project.description = form.cleaned_data['description']
        project.save()
        project_form = ProjectForm(instance = project)
      
      # otherwise, display the errors
      else:
        project_form = form
    
  # editing a cloned repository
  if 'clone_url' in request.POST:
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
  if 'repo_rss' in request.POST:
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
  if 'url' in request.POST:
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
  if 'switch-to-hosted' in request.POST:
    project.blog.from_feed = False
    project.blog.save()
      
  return render_to_response('projects/modify.html', {
    'project': project,
    'project_form': project_form,
    'cloned_repo_form': cloned_repo_form,
    'feed_repo_form': feed_repo_form,
    'blog_form': blog_form,
    'repo': project.repository,
    'tab': int(tab_id)
  }, context_instance = RequestContext(request))

# adds a user as an author of a project
def add_user(request):
  # get the user and project
  user = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))
  
  # don't let people add other users
  if int(request.user.id) is not user.id:
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.url_path,)))
  
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
  return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                      args = (project.url_path,)))

# removes a user as an author of a project
def remove_user(request):
  # get the user and project
  user = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))
  
  # don't let people delete other users
  if int(request.user.id) is not int(user.id):
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.url_path,)))
  
  # removes the user from the project
  if user in project.authors.all():
    project.authors.remove(user)
  
  # save
  project.save()
  
  # redirect back to the show page
  return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                      args = (project.url_path,)))

# displays the screenshot upload form
@login_required
def upload_screenshot(request, project_url_path):
  resp = force_url_paths('dashboard.views.projects.upload_screenshot',
                         project_url_path)
  if resp: return resp
  
  form = None
  project = get_object_or_404(Project, url_path = project_url_path)
  
  # if the user has submitted the form and is uploading a screenshot
  if request.method == 'POST':
    form = UploadScreenshotForm(request.POST, request.FILES)
    
    # if the form is valid, save the image and associate it with the project
    if form.is_valid():
      file = request.FILES["file"]
      
      # create a screenshot object in the database
      screen = Screenshot(title = form.cleaned_data["title"],
                          description = form.cleaned_data["description"],
                          project = project,
                          extension = os.path.splitext(file.name)[1])
      screen.save()
    
      # write the screenshot to a file
      path = os.path.join(SCREENSHOT_PATH, screen.filename())
      write = open(path, 'wb+')
      
      # write the chunks
      for chunk in file.chunks():
        write.write(chunk)
      write.close()
      
      # create a thumbnail of the file
      img = Image.open(path)
      
      # convert to a thumbnail
      img.thumbnail((240, 240), Image.ANTIALIAS)
      
      # save the thumbnail
      path = os.path.join(SCREENSHOT_PATH,
                          "{0}_t.png".format(str(screen.id)))
      img.save(path, "PNG")
      
      return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                          args = (project.url_path,)))
  
  # otherwise, create a new form
  else:
    form = UploadScreenshotForm()
  
  return render_to_response('projects/upload-screenshot.html', {
      'project': project,
      'form': form
    }, context_instance = RequestContext(request))

