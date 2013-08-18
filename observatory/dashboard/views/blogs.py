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

import datetime
from dashboard.forms import BlogPostForm, BlogForm
from dashboard.models import BlogPost, Blog, Project
from dashboard.util import url_pathify, force_url_paths
from dashboard.util import avoid_duplicate_queries
from dashboard.views import projects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from markdown import markdown

# the number of posts per page
POSTS_PER_PAGE = 5

# alias for the first page of blog posts
def posts(request):
  return posts_page(request, 1)

# shows a page of blog posts, the number of posts is set by PAGE_PER_POSTS
def posts_page(request, page_num):
  paginator = Paginator(BlogPost.objects.order_by('date').reverse(),
                        POSTS_PER_PAGE)
  
  # if the page requested does not exist, 404
  if int(page_num) not in paginator.page_range:
    raise Http404
  
  page = paginator.page(page_num)
  avoid_duplicate_queries(page.object_list, "author", "project",
                          author = { request.user.id: request.user }
                                   if request.user.is_authenticated() else {})
  
  # otherwise, render
  return render_to_response('blogs/posts.html', {
      'page': page,
      'disable_content': True
    }, context_instance = RequestContext(request))

# shows a project's internally hosted blog, or redirects to an external one
def show_blog(request, project_url_path):
  resp = force_url_paths(show_blog, project_url_path)
  if resp: return resp
  
  project = get_object_or_404(Project, url_path = project_url_path)
  if project.blog.from_feed:
    return HttpResponseRedirect(project.blog.url)
  else:
    return render_to_response('blogs/show-blog.html', {
        'project': project,
        'posts': project.blog.blogpost_set.all(),
        'disable_content': True
      }, context_instance = RequestContext(request))

# shows all blog posts by a specific user (personal blogs, mostly)
def show_user_blog(request, user_id):
  user = get_object_or_404(User, id = user_id)
  return render_to_response('blogs/show-user.html', {
      'posts': BlogPost.objects.filter(author = user),
      'user': user,
      'disable_content': True
    }, context_instance = RequestContext(request))

# shows a specific blog post
def show_post(request, project_url_path, post_url_path):
  resp = force_url_paths(show_post, project_url_path, post_url_path)
  if resp: return resp
  return show_post_real(request, post_url_path)

# show a post with a user-based url (personal posts)
def show_user_post(request, post_url_path):
  resp = force_url_paths(show_user_post, post_url_path)
  if resp: return resp
  return show_post_real(request, post_url_path)

# actually does the template/redirect for showing posts
def show_post_real(request, post_url_path):
  post = get_object_or_404(BlogPost, url_path = post_url_path)
  if post.from_feed:
    return HttpResponseRedirect(post.external_link)
  else:
    return render_to_response('blogs/show-post.html', {
        'post': post
      }, context_instance = RequestContext(request))

# write a new post
@login_required
def write_post(request, project_id):
  project = get_object_or_404(Project, id = int(project_id))
  if request.user not in project.authors.all():
    return HttpResponseRedirect(reverse(projects.show,
                                        args = (project.url_path,)))
  
  return render_to_response('blogs/edit.html', {
      'project': project,
      'form': BlogPostForm()
    }, context_instance = RequestContext(request))

# edit an existing post
@login_required
def edit_post(request, project_url_path, post_url_path):
  # redirect if the url path is not in the correct format
  resp = force_url_paths(edit_post, project_url_path, post_url_path)
  if resp: return resp
  
  post = get_object_or_404(BlogPost, url_path = post_url_path)
  
  if request.user not in post.blog.project.authors.all():
    return HttpResponseRedirect(reverse(projects.show,
                                        args = (project.url_path,)))
  
  return render_to_response('blogs/edit.html', {
      'project': post.blog.project,
      'post': post,
      'form': BlogPostForm(instance = post)
    }, context_instance = RequestContext(request))

# creates a new post
@login_required
def create_post(request, project_id):
  form = BlogPostForm(request.POST)
  project = get_object_or_404(Project, id = int(project_id))
  
  if request.user not in project.authors.all():
    return HttpResponseRedirect(reverse(projects.show,
                                        args = (project.url_path,)))
  
  # validate the form
  if form.is_valid():
    date = datetime.datetime.utcnow()
    html = markdown(request.POST['markdown'], safe_mode = "escape")
    post = BlogPost(title = request.POST['title'],
                    markdown = request.POST['markdown'],
                    summary = html,
                    content = html,
                    from_feed = False,
                    author = request.user,
                    project = project,
                    date = date)
    post.blog = project.blog
    post.save()
    
    project.blog.most_recent_date = date
    project.blog.save()
    project.calculate_score()
    
    return HttpResponseRedirect(reverse(show_post,
                                        args = (post.blog.project.url_path,
                                                post.url_path,)))
  else:
    return render_to_response('blogs/edit.html', {
        'project': project,
        'form': form
      }, context_instance = RequestContext(request)) 

# updates a previously posted post, and redirects to the management page
@login_required
def update_post(request, project_url_path, post_url_path):
  form = BlogPostForm(request.POST)
  post = get_object_or_404(BlogPost, url_path = post_url_path)
  
  # validate the form
  if form.is_valid():
    # update the post
    html = markdown(request.POST['markdown'], safe_mode = "escape")
    post.title = request.POST['title']
    post.markdown = request.POST['markdown']
    post.summary = html
    post.content = html
    post.save()
    
    return HttpResponseRedirect(reverse(show_post,
                                        args = (post.blog.project.url_path,
                                                post.url_path,)))
  else:
    return render_to_response('blogs/edit.html', {
        'project': post.blog.project,
        'form': form
      }, context_instance = RequestContext(request))

# deletes a post
@login_required
def delete_post(request, project_url_path, post_url_path):
  post = get_object_or_404(BlogPost, url_path = post_url_path)
  project = post.project
  
  if request.user not in post.blog.project.authors.all():
    return HttpResponseRedirect(reverse(projects.show,
                                        args = (project.url_path,)))
  post.delete()
  return HttpResponseRedirect(reverse(projects.modify,
                                      args = (project.url_path, 2)))

@login_required
def remove_personal_blog(request, user_id):
  if request.user.id != int(user_id):
    raise Http404
  
  try: #remove the blog and all related posts, if they have one
    blog = Blog.objects.get(user = request.user)
    BlogPost.objects.filter(blog = blog).delete()
    blog.delete()
  except Blog.DoesNotExist:
    pass #No need to delete anything

  from dashboard.views import users
  return HttpResponseRedirect(reverse(users.profile,
                                      args = (request.user.id,)))

@login_required
def edit_personal_blog(request, user_id):
  # users can only edit their own blogs, of course
  if request.user.id != int(user_id):
    raise Http404
  
  # user is saving the form
  if request.POST:
    form = BlogForm(request.POST)
    if form.is_valid():
      try:
        blog = Blog.objects.get(user = request.user)
        blog.url = form.cleaned_data['url']
        blog.rss = form.cleaned_data['rss']
      except Blog.DoesNotExist:
        blog = Blog(user = request.user,
                    url = form.cleaned_data['url'],
                    rss = form.cleaned_data['rss'],
                    from_feed = True)
      blog.save()
    
    # prevent form resubmission on refresh by redirecting
    from dashboard.views import users
    return HttpResponseRedirect(reverse(users.profile,
                                        args = (request.user.id,)))
  
  # displaying the initial form, or a form from an already created blog
  else:
    try:
      form = BlogForm(instance = Blog.objects.get(user = request.user))
    except Blog.DoesNotExist:
      form = BlogForm()
  
  return render_to_response("blogs/edit-personal-blog.html", {
      "form": form,
      "user": request.user,
    }, context_instance = RequestContext(request))
