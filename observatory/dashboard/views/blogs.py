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

from dashboard.models import BlogPost
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

# the number of posts per page
POSTS_PER_PAGE = 5

# alias for the first page of blog posts
def posts(request):
  return posts_page(request, 1)

# shows a page of blog posts, the number of posts is set by PAGE_PER_POSTS
def posts_page(request, page_num):
  paginator = Paginator(BlogPost.objects.all().order_by('date').reverse(),
                        POSTS_PER_PAGE)
  
  # if the page requested does not exist, 404
  if int(page_num) not in paginator.page_range:
    raise Http404
  
  # otherwise, render
  return render_to_response('blogs/posts.html', {
      'page': paginator.page(page_num)
    }, context_instance = RequestContext(request))

# shows a specific blog post
def show_post(request, post_id):
  return render_to_response('blogs/show-post.html', {
      'post': get_object_or_404(BlogPost, id = int(post_id))
    }, context_instance = RequestContext(request))