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
from ..util import time_ago

# an event is currently either a blog post or a commit
class Event(models.Model):
  class Meta:
    app_label = 'dashboard'
  
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