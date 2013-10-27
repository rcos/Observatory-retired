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
import re
from dashboard.util import sanitize
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
import feedparser
import dateutil.parser
from EventSet import EventSet

# a blog for a project
class Blog(EventSet):
  class Meta:
    app_label = 'dashboard'
  
  # link to the blog, if it isn't hosted on dashboard
  url = models.URLField("Blog Web Address")
  rss = models.URLField("Blog Feed")
  
  # the user associated with the blog, if it is a personal blog
  user = models.ForeignKey(User, blank = True, null = True)
  
  # returns the address for the blog, which depends on whether or not it
  # is hosted internally or externally
  def link_to(self):
    if self.from_feed:
      return self.url
    else:
      from dashboard.views import blogs
      return reverse(blogs.show_blog, args = (self.project.url_path,))
  
  # fetches the posts from the rss feed
  def fetch(self):
    import BlogPost
    
    # don't fetch internally hosted blogs
    if not self.from_feed: return
    
    events = []
    
    # parse and iterate the feed
    entries = feedparser.parse(self.rss).entries
    for post in entries:
      try:
        date = dateutil.parser.parse(post.published).replace(tzinfo=None)
      except:
        try:
            date = dateutil.parser.parse(post.created).replace(tzinfo=None)
        except:
            return
      
      # don't re-add old posts
      if self.most_recent_date >= date:
        continue
      
      try:
        content = post.content[0].value
      except:
        content = post.description
      
      try:
        author_name = post.author_detail["name"]
      except:
        author_name = None
      
      # sanitize the post's content
      content = sanitize(content, [
        "h1", "h2", "h3", "h4", "h5", "h6",
        "a:href", "p", "ul", "ol", "li", "br", "div",
        "img:src:alt:title",
        "b", "i", "u", "strong", "em",
        "table", "tbody", "td", "th", "thead", "tfoot",
        "pre", "tt", "code"
      ])
      
      # format a summary for the post
      summary = sanitize(content, [], strip_tags = [
        "h1", "h2", "h3", "h4", "h5", "h6",
        "p", "ul", "ol", "li", "br", "div", 'a',
        "b", "i", "u", "strong", "em",
        "pre", "tt", "code"
      ])
      
      if len(summary) > 500:
        summary = summary[0:500] + u"..."
      summary = "<p>" + summary + "</p>"
      
      events.append(self.add_event(BlogPost.BlogPost,
        title = post.title,
        summary = summary,
        from_feed = True,
        author_name = author_name,
        date = date,
        extra_args = {
          "external_link": post.link,
          "content": content,
          "blog_id": self.id
        }
      ))
    
    # find the new most recent date
    dates = [event.date for event in events if event is not None]
    dates.append(self.most_recent_date)
    self.most_recent_date = max(dates)
    self.save()
