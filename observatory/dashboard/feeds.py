# coding=utf8

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

import re
from dashboard.models import *
from dashboard.util import url_pathify
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from dashboard import views
from observatory.settings import DOMAIN_NAME, FEED_TITLE
from observatory.settings import FEED_COUNT, PROJECT_FEED_COUNT
from urlparse import urljoin as join

def strip_extra_whitespace(string):
  return re.sub("[ \t\n]+", " ", string).strip()
  
class DashboardFeed(Feed):
  def item_title(self, event):
    return event.title

  def item_description(self, event):
    return event.summary

  def item_author_name(self, event):
    if event.author is not None:
      return event.author.get_full_name()
    elif event.author_name is not None:
      return event.author_name
    else:
      return u"Authors of {0}".format(event.project.title)
  
  def item_author_link(self, event):
    if event.project:
      return event.project.website
    else:
      return None
  
  def item_pubdate(self, event):
    return event.date
  
  def item_link(self, event):
    return join(DOMAIN_NAME, reverse(views.feed.event,
                                     args = (event.url_path,)))

class SingleFeed(DashboardFeed):
  model = None
  
  def get_object(self, request, project = None, url_path = None, model = None):
    self.model = model
    self.project = get_object_or_404(Project, url_path = url_pathify(project))
    self.url_path = url_path
    self.object = self.model.objects.get(project = self.project,
                                         url_path = url_pathify(url_path))
  
  def items(self):
    return [self.object]
  
  def title(self):
    string = u"{0} • {1} • {2}".format(FEED_TITLE,
                                       self.project.title,
                                       self.object.title)
    return strip_extra_whitespace(string)

  def description(self):
    return self.object.summary

  def link(self):
    if self.model == Commit:
      return join(DOMAIN_NAME, reverse(views.commits.show_repository,
                                       args = (self.project.url_path,)))
    else:
      return join(DOMAIN_NAME, reverse(views.blogs.show_blog,
                                  args = (self.project.url_path,)))

class PluralFeed(DashboardFeed):
  def get_object(self, request, project = None):
    if project is not None:
      self.project = get_object_or_404(Project, url_path=url_pathify(project))
    else:
      self.project = None
  
  def items(self):
    if self.project is not None:
      events = self.model.objects.filter(project = self.project)
      return events.order_by("-date")[:PROJECT_FEED_COUNT]
    else:
      return self.model.objects.order_by("-date")[:FEED_COUNT]

class EventsFeed(PluralFeed):
  model = Event
  
  def title(self):
    if self.project is not None:
      string = u"{0} • {1}'s Events".format(FEED_TITLE, self.project.title)
    else:
      return FEED_TITLE
    return strip_extra_whitespace(string)
  
  def description(self):
    if self.project is not None:
      return self.project.description
    else:
      return u"All events tracked by {0}.".format(FEED_TITLE)
  
  def link(self):
    if self.project is not None:
      return join(DOMAIN_NAME, reverse(views.projects.show,
                                  args = (self.project.url_path,)))
    else:
      return join(DOMAIN_NAME, reverse(views.feed.feed))
  
class CommitsFeed(PluralFeed):
  model = Commit
  
  def title(self):
    if self.project is not None:
      string = u"{0} • commits in {1}".format(FEED_TITLE, self.project.title)
    else:
      string = u"{0} • Commits".format(FEED_TITLE)
    return strip_extra_whitespace(string)
  
  def description(self):
    if self.project is not None:
      return self.project.description
    else:
      return u"All commits tracked by {0}.".format(FEED_TITLE)
  
  def link(self):
    if self.project is not None:
      return join(DOMAIN_NAME, reverse(views.commits.show_repository,
                                  args = (self.project.url_path,)))
    else:
      return join(DOMAIN_NAME, reverse(views.commits.all))
  
class BlogPostsFeed(PluralFeed):
  model = BlogPost
  
  def title(self):
    if self.project is not None:
      string = u"{0} • posts about {1}".format(FEED_TITLE, self.project.title)
    else:
      string = u"{0} • Posts".format(FEED_TITLE)
    return strip_extra_whitespace(string)
  
  def description(self):
    if self.project is not None:
      return self.project.description
    else:
      return u"All posts tracked by {0}.".format(FEED_TITLE)
  
  def link(self):
    if self.project is not None:
      return join(DOMAIN_NAME, reverse(views.blogs.show_blog,
                                  args = (self.project.url_path,)))
    else:
      return join(DOMAIN_NAME, reverse(views.blogs.posts))
