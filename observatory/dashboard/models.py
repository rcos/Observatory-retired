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
import os
from django.db import models
from django.contrib.auth.models import User
from lib import feedparser, dateutil
from settings import SCREENSHOT_URL

# an event is currently either a blog post or a commit
class Event(models.Model):
  # title of the event
  title = models.CharField("Title", max_length = 128)
  
  # when the event occured
  date = models.DateTimeField()
  
  # the description is the main content for the event
  description = models.TextField()

# a blog for a project
class Blog(models.Model):
  # link to the blog, if it isn't hosted on dashboard
  url = models.URLField("Blog Web Address", max_length = 64)
  rss = models.URLField("Blog Feed", max_length = 64)
  
  # external (from an rss feed)? or hosted by dashboard?
  external = models.BooleanField()
  
  # fetches the posts from the rss feed
  def fetch(self):
    # don't fetch internally hosted blogs
    if not external: return
    
    # make sure we can add blogposts to the blog
    self.save()
    
    # parse and iterate the feed
    for post in feedparser.parse(self.rss).entries:
      # time manipation is fun
      date = dateutil.parser.parse(post.date)
      date = (date - date.utcoffset()).replace(tzinfo=None)
      
      post = BlogPost(title = post.title,
                      description = post.description,
                      summary = post.description,
                      date = date,
                      external = True)
      post.blog = self
      post.save()
    self.save()
  
# a post in a blog
class BlogPost(Event):
  # the text of the post
  markdown = models.TextField("Content")
  summary = models.TextField()
  
  # posts can be internal on external blogs (vice versa) if the blog switches
  external = models.BooleanField()
  
  # what blog the post is associated with
  blog = models.ForeignKey(Blog)
  
# a version control repository
class Repository(models.Model):
  # web access to the repository
  web_url = models.URLField("Repository Web Address", max_length = 128)
  
  # cloned repository fields
  clone_url = models.URLField("Repository Clone Address", max_length = 128)
  vcs = models.CharField("Version Control System", max_length = 3,
                         default = 'git',
                         choices = (('git', 'git'),
                                    ('svn', 'Subversion'),
                                    ('hg',  'Mercurial'),
                                    ('bzr', 'Bazaar')))
  
  # non-cloned repository fields
  repo_rss = models.URLField("Repository RSS Feed", max_length = 128)
  cmd = models.CharField("Clone Command", max_length = 128)
  
  # whether the repo uses cloning or just an rss feed
  cloned = models.BooleanField()
  
  def fetch(self):
    if self.cloned:
      pass
    else:
      for commit in feedparser.parse(self.repo_rss).entries:
        date = dateutil.parser.parse(commit.date)
        date = (date - date.utcoffset()).replace(tzinfo=None)
        
        # can we find an author for this commit?
        author_name = commit.author_detail['name']
        print author_name
        try:
          author_firstlast = author_name.split(' ')
          print author_firstlast
          authors = User.objects.filter(first_name = author_firstlast[0],
                                        last_name = author_firstlast[1])
          print authors
          if len(authors) is 1:
            author = authors[0]
          else:
            author = None
        except:
          author = None
        
        # create and save the commit object
        commit = Commit(author_name = author_name,
                        title = commit.title,
                        description = commit.description,
                        url = commit.link,
                        date = date)
        commit.repository = self
        if author is not None:
          commit.author = author
        commit.save()
  
  def clone_cmd(self):
    if self.cloned:
      cmds = { 'git': 'clone', 'svn': 'co', 'hg': 'clone', 'bzr': 'branch' }
      return '{0} {1} {2}'.format(self.vcs, cmds[self.vcs], self.clone_url)
    else:
      return self.cmd
  
  def __unicode__(self):
    return self.web_url

# a commit in a repository
class Commit(Event):
  # the url to the commit (in cgit, etc.)
  url = models.URLField("Commit URL", max_length = 200, blank = True)

  # the author of the commit, if he/she is in dashboard
  author = models.ForeignKey(User, blank = True, null = True)

  # the author's name, if he/she isn't in dashboard
  author_name = models.CharField(max_length = 64, blank = True, null = True)
  
  # the diff for the commit. This won't exist for RSS commits
  diff = models.TextField(blank = True, null = True)

  # the repository the commit is part of
  repository = models.ForeignKey(Repository)

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

# a screenshot for a project, display on its page. its filename is derived from
# its ID, so it is not required as a field
class Screenshot(models.Model):
  # the title of the screenshot
  title = models.CharField(max_length = 32)

  # a short description of the screenshot
  description = models.CharField(max_length = 100)
  
  # what project is this a screenshot of?
  project = models.ForeignKey(Project)
  
  # file extension
  extension = models.CharField(max_length = 8)
  
  # the filename for this file. just the last part, no directory specified.
  def filename(self):
    return "{0}{1}".format(str(self.id), self.extension)
  
  # the thumbnail filename for this file, no directory specified.
  def thumbnail(self):
    return str(self.id) + "_t.png"
  
  # the url of a screenshot
  def url(self):
    return os.path.join(SCREENSHOT_URL, self.filename())
  
  # the thumbnail url of a screenshot
  def thumb_url(self):
    return os.path.join(SCREENSHOT_URL, self.thumbnail())
