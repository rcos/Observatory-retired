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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from dashboard.models import *
from dashboard.forms import *
from dashboard.util import ListPaginator
from settings import SCREENSHOT_PATH
import Image
import os

# index and list are temporarily the same
def index(request):
  return list(request)

# the classic "dashboard" view, with rankings
def list(request):
  return render_to_response('projects/index.html', {
      'projects': Project.objects.all()
    }, context_instance = RequestContext(request))

# information about a specific project
def show(request, project_id):  
  # get the project
  project = get_object_or_404(Project, id = int(project_id))
  
  # create a paginated list of the screenshots of the project
  paginator = None
  screenshots = Screenshot.objects.filter(project = project)
  if screenshots.count > 0:
    paginator = ListPaginator(screenshots.order_by('id').reverse(), 3)
  
  return render_to_response('projects/show.html', {
      'project': project,
      'paginator': paginator,
      'default_page': 1,
      'has_screenshots': len(screenshots) > 0
    }, context_instance = RequestContext(request))

# a view for adding a new project
@login_required
def add(request):
  form_parts = {
    0: lambda: True,
    1: lambda: len(request.POST['wiki']) > 0 and
               len(request.POST['website']) > 0 and
               len(request.POST['title']) > 0 and
               len(request.POST['description']) > 0,
    2: lambda: len(request.POST['web_url']) > 0 and
                (('clone_url' in request.POST and
                  len(request.POST['clone_url']) > 0) or
                 ('repo_rss' in request.POST and
                  len(request.POST['repo_rss']) > 0 and
                  len(request.POST['cmd']) > 0)),
    3: lambda: 'rss' not in request.POST or
               (len(request.POST['rss']) > 0 and
                len(request.POST['url']) > 0)
  }
  
  form_keys = {
    1: ('title', 'description', 'website', 'wiki'),
    2: ('web_url', 'clone_url', 'vcs', 'repo_rss', 'cmd'),
    3: ('url', 'rss')
  }
  
  if 'current' in request.POST:
    current = int(request.POST['current']) + 1
  else:
    current = 1
  
  # validate the previous form and return to it with errors if needed
  if form_parts[current - 1]():
    repo_form = RepositoryForm()
    project_form = ProjectForm()
    blog_form = BlogForm()
  else:
    repo_form = RepositoryForm(request.POST)
    project_form = ProjectForm(request.POST)
    blog_form = BlogForm(request.POST)
    current -= 1
  
  # if there are more parts to the form
  if current < len(form_parts):
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
        'parts': form_parts,
        'current': current,
        'previous_data': post,
        'repo_form': repo_form,
        'project_form': project_form,
        'blog_form': blog_form
      }, context_instance = RequestContext(request))
  
  # otherwise, if the form is complete, create the project
  else:
    # create the blog object
    if 'rss' in request.POST:
      blog = Blog(url = request.POST['url'],
                  rss = request.POST['rss'],
                  external = True)
      blog.fetch()
    else:
      blog = Blog(external = False)
    blog.save()

    # create the repository object
    if 'clone_url' in request.POST:
      repo = Repository(web_url = request.POST['web_url'],
                        clone_url = request.POST['clone_url'],
                        cloned = True)
    else:
      repo = Repository(web_url = request.POST['web_url'],
                        repo_rss = request.POST['repo_rss'],
                        cloned = False)
    repo.save()

    # create the project object
    project = Project(title = request.POST['title'],
                      website = request.POST['website'],
                      wiki = request.POST['wiki'],
                      description = request.POST['description'],
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
                                        args = (project.id,)))

# a view for modifying an existing project
@login_required
def modify(request, project_id):
  project = get_object_or_404(Project, id = int(project_id))
  
  # if someone tries to edit a project they shouldn't, send them to the
  # the default project view page
  if request.user not in project.authors.all():
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.id,)))
  
  return render_to_response('projects/modify.html', {
    'project': project,
    'form': ProjectForm(project)
  }, context_instance = RequestContext(request))

# saves an existing project and redirects to its information page
@login_required
def update(request, project_id):
  project = get_object_or_404(Project, id = int(project_id))
  
  # if someone tries to edit a project they shouldn't, send them to the
  # the default project view page
  if request.user not in project.authors.all():
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.id,)))
  
  # find the RSS feeds
  response, blog_rss, repo_rss = find_feeds(request,
                                            'dashboard.views.projects.update',
                                            args = (project.id,))

  # if a response was created, return it
  if response is not None:
    return response
  
  # update the project
  project.title = request.POST['title']
  project.website = request.POST['website']
  project.blog.url = request.POST['blog']
  project.repository.url = request.POST['repository']
  project.wiki = request.POST['wiki']
  project.active = 'active' in request.POST
  project.description = request.POST['description']
  
  # save the project
  project.save()
  project.blog.save()
  project.repository.save()
  
  return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                      args = (project.id,)))

# adds a user as an author of a project
def add_user(request):
  # get the user and project
  user = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))
  
  # don't let people add other users
  if int(request.user.id) is not user.id:
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.id,)))
  
  # add the user to the project
  if user not in project.authors.all():
    project.authors.add(user)
  
  # save
  project.save()
  
  # redirect back to the show page
  return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                      args = (project.id,)))

# removes a user as an author of a project
def remove_user(request):
  # get the user and project
  user = get_object_or_404(User, id = int(request.POST["user_id"]))
  project = get_object_or_404(Project, id = int(request.POST["project_id"]))
  
  # don't let people delete other users
  if int(request.user.id) is not int(user.id):
    return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                        args = (project.id,)))
  
  # removes the user from the project
  if user in project.authors.all():
    project.authors.remove(user)
  
  # save
  project.save()
  
  # redirect back to the show page
  return HttpResponseRedirect(reverse('dashboard.views.projects.show',
                                      args = (project.id,)))

# displays the screenshot upload form
def upload_screenshot(request, project_id):
  form = None
  project = get_object_or_404(Project, id = project_id)
  
  # if the user has submitted the form and is uploading a screenshot
  if request.method == 'POST':
    form = UploadScreenshotForm(request.POST, request.FILES)
    
    # if the form is valid, save the image and associate it with the project
    if form.is_valid():
      file = request.FILES["file"]
      
      # create a screenshot object in the database
      screen = Screenshot(title = request.POST["title"],
                          description = request.POST["description"],
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
                                          args = (project.id,)))
  
  # otherwise, create a new form
  else:
    form = UploadScreenshotForm()
  
  return render_to_response('projects/upload-screenshot.html', {
      'project': project,
      'form': form
    }, context_instance = RequestContext(request))

