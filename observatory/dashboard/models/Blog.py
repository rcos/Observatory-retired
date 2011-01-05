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

from django.db import models
from django.contrib.auth.models import User
from lib import feedparser, dateutil
from EventSet import EventSet

# a blog for a project
class Blog(EventSet):
  class Meta:
    app_label = 'dashboard'
  
  # link to the blog, if it isn't hosted on dashboard
  url = models.URLField("Blog Web Address", max_length = 64)
  rss = models.URLField("Blog Feed", max_length = 64)
  
  # external (from an rss feed)? or hosted by dashboard?
  external = models.BooleanField()
  
  # fetches the posts from the rss feed
  def fetch(self):
    # don't fetch internally hosted blogs
    if not self.external: return
    
    # make sure we can add blogposts to the blog
    self.save()
    
    # parse and iterate the feed
    max_date = self.most_recent_date
    for post in feedparser.parse(self.rss).entries:
      # time manipation is fun
      date = dateutil.parser.parse(post.date)
      try:
        date = (date - date.utcoffset()).replace(tzinfo=None)
      except:
        pass
      
      # find the new most recently updated date
      if max_date < date:
        max_date = date
      
      # don't re-add old posts
      if self.most_recent_date >= date:
        continue
      
      # can we find an author for this blog post?
      try:
        author_name = post.author_details['name']
        author_firstlast = author_name.split(' ')
        authors = User.objects.filter(first_name = author_firstlast[0],
                                      last_name = author_firstlast[1])
        if len(authors) is 1:
          author = authors[0]
        else:
          author = None
      except:
        author_name = None
        author = None
      
      try:
        description = post.content[0].value
      except:
        description = post.description
      
      import BlogPost
      post = BlogPost.BlogPost(author_name = author_name,
                               title = post.title,
                               description = description,
                               summary = post.description,
                               date = date,
                               external_link = post.link,
                               external = True)
      post.blog = self
      if author is not None:
        post.author = author
      post.save()
      
      # print out results
      print "Post by {0} in {1} at {2}".format(author_name,
                                               self.project.title,
                                               date)
    self.most_recent_date = max_date
    self.save()