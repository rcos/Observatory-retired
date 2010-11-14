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

import datetime
from django.db import models
from django.contrib.auth.models import User
from lib import feedparser, dateutil

# a blog for a project
class Blog(models.Model):
  url = models.URLField(max_length = 64)
  rss = models.URLField("Blog RSS Feed", max_length = 64)
  
  # fetches the posts from the rss feed, also saves the Blog to ensure it has
  # a key before attempting to add BlogPosts to it
  def fetch(self):
    self.save()
    
    # parse and iterate the feed
    for post in feedparser.parse(self.rss).entries:
      # time manipation is fun
      date = dateutil.parser.parse(post.date)
      date = (date - date.utcoffset()).replace(tzinfo=None)
      
      post = BlogPost(title = post.title,
                      content = post.description,
                      summary = post.description,
                      date = date)
      post.blog = self
      post.save()
    self.save()
  
# a post in a blog
class BlogPost(models.Model):
  # title of the post
  title = models.CharField(max_length = 128)
  
  # the text of the post
  content = models.TextField()
  summary = models.TextField()
  
  # when the post was made
  date = models.DateTimeField()
  
  # what blog the post is associated with
  blog = models.ForeignKey(Blog)
  
# a version control repository
class Repository(models.Model):
  # version control
  url = models.URLField("Source URL", max_length = 64)
  checkout = models.URLField("Source Checkout URL", max_length = 64)
  
  # rss feed (for now, won't work with branches so fundamentally broken)
  rss = models.URLField("Repository RSS Feed", max_length = 64)

# a commit in a repository
class Commit(models.Model):
  # the url to the commit (in cgit, etc.)
  url = models.URLField("Commit URL", max_length = 200)

  # the author of the commit, if he/she is in dashboard
  author = models.ForeignKey(User)

  # the author's name, if he/she isn't in dashboard
  author_name = models.CharField(max_length = 64)

  # the repository the commit is part of
  respository = models.ForeignKey(Repository)

# an RCOS project
class Project(models.Model):  
  # basic things
  title = models.CharField(max_length = 32)
  
  # a short description of the project
  description = models.TextField()
  
  # project's web presence
  website = models.URLField(max_length = 64)
  
  # version control
  repository = models.OneToOneField(Repository)
  
  # blog
  blog = models.OneToOneField(Blog)
  
  # wiki
  wiki = models.URLField(max_length = 64)
  
  # authors of the project
  authors = models.ManyToManyField(User)
  
  # if the project is currently active
  active = models.BooleanField("Currently Active")
  
  # string representation of the project
  def __unicode__(self):
    return self.title