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
from dashboard.util import time_ago, url_pathify_safe
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from Project import Project
from URLPathedModel import URLPathedModel
from model_utils.managers import InheritanceManager

# an event is currently either a blog post or a commit
class Event(URLPathedModel):
  class Meta:
    app_label = 'dashboard'

  # Overload objects to give us the select_subclasses option
  objects = InheritanceManager()

  # title of the event
  title = models.CharField("Title", max_length = 128)
  
  # when the event occured
  date = models.DateTimeField()
  
  # a short (hopefully) summary of the event's content.
  # more specific data is stored in the subclasses, Commit and BlogPost
  summary = models.TextField()
  
  # whether the event's source is from a feed
  from_feed = models.BooleanField()
  
  # the project associated with the Event
  project = models.ForeignKey(Project, blank = True, null = True)
  
  # the author of the event, if he/she is in dashboard
  author = models.ForeignKey(User, blank = True, null = True)

  # the author's name, displayed if he/she isn't in dashboard
  author_name = models.CharField(max_length = 64, blank = True, null = True)
  
  # the author's email
  author_email = models.CharField(max_length = 64, blank = True, null = True)
  
  def __unicode__(self):
    return self.title
  
  # format the summary for display
  def formatted_summary(self):
    return self.summary
  
  # assign the url path when the event is first created
  def save(self, *args, **kwargs):
    # ensure that the title, email, and name fields are not too long
    if len(self.title) > 128:
      self.title = self.title[0:125] + "..."
    
    if self.author_email is not None and len(self.author_email) > 64:
      self.author_email = self.author_email[0:61] + "..."
    
    if self.author_name is not None and len(self.author_name) > 64:
      self.author_name = self.author_name[0:61] + "..."
    
    super(Event, self).save(*args, **kwargs)
  
  # the name of the event type, by default this is just the class name
  def type_name(self):
    return self.__class__.__name__
  
  # how old the event is (relative to now by default)
  def age(self, time = None):
    if time is None:
      time = datetime.datetime.utcnow()
    return time_ago(self.date, time)

