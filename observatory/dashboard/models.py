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

import colorsys
import datetime
import os
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from lib import feedparser, dateutil
from settings import SCREENSHOT_URL
from util import time_ago

# an event is currently either a blog post or a commit
class Event(models.Model):
  # title of the event
  title = models.CharField("Title", max_length = 128)
  
  # when the event occured
  date = models.DateTimeField()
  
  # the description is the main content for the event
  description = models.TextField()
  
  # the author of the event, if he/she is in dashboard
  author = models.ForeignKey(User, blank = True, null = True)

  # the author's name, if he/she isn't in dashboard
  author_name = models.CharField(max_length = 64, blank = True, null = True)
  
  # whether or not the description should be autoescaped
  def autoescape(self):
    return True
  
  # the tags that should wrap the description when displayed
  def wrap_tags(self):
    return None
  
  # the name of the event type, by default this is just the class name
  def type_name(self):
    return self.__class__.__name__
  
  # how old the event is (relative to now by default)
  def age(self, time = datetime.datetime.now()):
    return time_ago(self.date, time)
  
  # a link to more details on the event
  def link(self):
    return None

# a set of events (a blog or repository)
class EventSet(models.Model):
  # most recent time to add new events for
  most_recent_date = models.DateTimeField(default = datetime.datetime(1, 1, 1))
  
  # how recent was the last update?
  def age_ago(self, time = datetime.datetime.now()):
    return time_ago(self.most_recent_date, time)
  
  # when was this eventset last updated?
  def when_updated(self):
    if self.most_recent_date != datetime.datetime(1, 1, 1):
      return "{0} updated {1}".format(self.__class__.__name__, self.age_ago())
    else:
      return "{0} never updated".format(self.__class__.__name__,
                                        self.age_ago())
  
  class Meta:
    abstract = True

# a blog for a project
class Blog(EventSet):
  # link to the blog, if it isn't hosted on dashboard
  url = models.URLField("Blog Web Address", max_length = 64)
  rss = models.URLField("Blog Feed", max_length = 64)
  
  # external (from an rss feed)? or hosted by dashboard?
  external = models.BooleanField()
  
  # how recent was the last post?
  def age_ago(self, time = datetime.datetime.now()):
    return time_ago(self.most_recent_date, time)
  
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
      date = (date - date.utcoffset()).replace(tzinfo=None)
      
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
      
      post = BlogPost(author_name = author_name,
                      title = post.title,
                      description = post.description,
                      summary = post.description,
                      date = date,
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
  
# a post in a blog
class BlogPost(Event):
  # the text of the post
  markdown = models.TextField("Content")
  summary = models.TextField()
  
  # posts can be internal on external blogs (vice versa) if the blog switches
  external = models.BooleanField()
  
  # what blog the post is associated with
  blog = models.ForeignKey(Blog)
  
  def project(self):
    return self.blog.project
    
  def autoescape(self):
    return False
  
  def type_name(self):
    return "Post"
  
  def link(self):
    return reverse('dashboard.views.blogs.show_post', args = (self.id,))
  
# a version control repository
class Repository(EventSet):
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
      max_date = self.most_recent_date
      for commit in feedparser.parse(self.repo_rss).entries:
        date = dateutil.parser.parse(commit.date)
        date = (date - date.utcoffset()).replace(tzinfo=None)

        # find the new most recently updated date
        if max_date < date:
          max_date = date
        
        # don't re-add old commits
        if self.most_recent_date >= date:
          continue
        
        # can we find an author for this commit?
        author_name = commit.author_detail['name']
        try:
          author_firstlast = author_name.split(' ')
          authors = User.objects.filter(first_name = author_firstlast[0],
                                        last_name = author_firstlast[1])
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
        
        # print out results
        print "Commit by {0} in {1} at {2}".format(author_name,
                                                   self.project.title,
                                                   date)
        
      self.most_recent_date = max_date
      self.save()
  
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
  
  # the diff for the commit. This won't exist for RSS commits
  diff = models.TextField(blank = True, null = True)

  # the repository the commit is part of
  repository = models.ForeignKey(Repository)
  
  def autoescape(self):
    return False
  
  def project(self):
    return self.repository.project
    
  def wrap_tags(self):
    if self.description.find('<pre>') is -1:
      return ['p', 'pre']
    else:
      return ['p']
  
  def wrap_tags_rev(self):
    tags = self.wrap_tags()
    tags.reverse()
    return tags
  
  def link(self):
    if self.repository.cloned:
      return None
    else:
      return self.url
    
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
  
  # the score of the project, computed after each fetch
  score = models.FloatField(blank = True, null = True)
  
  # the rank of the project, computed after each fetch
  rank = models.IntegerField(blank = True, null = True)
  
  # fetch and update the project's blog and repository
  def fetch(self):
    self.blog.fetch()
    self.repository.fetch()
    
    # determine the score of the project
    now = datetime.datetime.now()
    r = (now - self.repository.most_recent_date).seconds
    b = (now - self.blog.most_recent_date).seconds
    self.score = (r * r + r * b + b * b + r) / 1000000
    self.save()
  
  # string representation of the project
  def __unicode__(self):
    return self.title
  
  # CSS for background of ranking emblem
  def rank_emblem_css(self):
    # a bit inefficient?
    count = float(len(Project.objects.all()))
    hue = self.rank / count
    mainbg = colorsys.hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.75)
    lightbg = colorsys.hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.9)
    darkbg = colorsys.hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.6)
    inset = colorsys.hsv_to_rgb(0.3 - hue * 0.3, 0.5, 0.2)
    
    return """
      background:rgb({0},{1},{2});
      background-image: -webkit-gradient(linear, left bottom, left top,
        from(rgb({0},{1},{2})),
        to(rgb({9},{10},{11})));
      background-image: -moz-linear-gradient(100% 100% 90deg,
        rgb({0},{1},{2}),
        rgb({9},{10},{11})
      );
      -moz-text-shadow: 0px -1px 1px rgb({6},{7},{8});
      -webkit-text-shadow: 0px -1px 1px rgb({6},{7},{8});
      text-shadow: 0px -1px 1px rgb({6},{7},{8});
      """.format(int(mainbg[0] * 255),
                 int(mainbg[1] * 255),
                 int(mainbg[2] * 255),
                 int(darkbg[0] * 255),
                 int(darkbg[1] * 255),
                 int(darkbg[2] * 255),
                 int(inset[0] * 255),
                 int(inset[1] * 255),
                 int(inset[2] * 255),
                 int(lightbg[0] * 255),
                 int(lightbg[1] * 255),
                 int(lightbg[2] * 255))

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
