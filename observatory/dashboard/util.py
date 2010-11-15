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

from collections import defaultdict
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from HTMLParser import HTMLParser
from urllib import urlopen

# finds the feeds for blog and repo, or make the user input them
def find_feeds(request, next, args = None):
  def find_rss(url):
    # try to find an rss feed
    try:
      return RSSFinder().find(urlopen(url).read())

    # alright, this is a silent failure. is it good to show potentially complex
    # error message to the user or is it better to just say "hey, we can't find
    # your feed, can you just give it to us?"
    except:
      return None
  
  # if the user manually entered the blog feed, use that URL
  if 'blog_rss' in request.POST:
    blog_rss = request.POST['blog_rss']
  else:
    # attempt to find the project's blog rss feed
    blog_rss = find_rss(request.POST['blog'])
  
  # if the user manually entered the repo feed, use that URL
  if 'repo_rss' in request.POST:
    repo_rss = request.POST['repo_rss']
  else:
    # attempt to find the project's repo rss feed
    repo_rss = find_rss(request.POST['repository'])
  
  # if the automatic finding didn't work, require the user to input the feeds
  if repo_rss is None or blog_rss is None:
    single = not (repo_rss is None and blog_rss is None)
    
    error_header = "We couldn't find your feeds."
    if single:
      if repo_rss:
        error_header = "We couldn't find your blog feed."
      else:
        error_header = "We couldn't find your repository feed."
    
    return render_to_response('projects/rss-feeds.html', {
        'post': request.POST,
        'repo_rss': repo_rss,
        'blog_rss': blog_rss,
        'next': reverse(next, args = args),
        'single': single,
        'error_header': error_header
      }, context_instance = RequestContext(request)), blog_rss, repo_rss;
  
  # otherwise, return None and the located feeds
  return None, blog_rss, repo_rss

# an HTMLParser subclass for locating RSS feeds in HTML files
class RSSFinder(HTMLParser):
  rss_feed = None
  
  def find(self, html):
    self.feed(html)
    self.close()
    return self.rss_feed
  
  def handle_starttag(self, tag, attrs):
    # only both with link tags (if we haven't already)
    if tag == 'link':
      link = None
      is_rss = False
      
      # iterate over the attributes
      for (name, data) in attrs:
        # if it is the link tag, set the link
        if name == 'href':
          link = data
        
        # this is an RSS tag!
        elif (data == 'application/rss+xml' or
              data == 'application/atom+xml' and
              name == 'type'):
          is_rss = True
      
      # if an RSS feed was found, set it in the outer scope
      if is_rss and data is not None:
        self.rss_feed = link