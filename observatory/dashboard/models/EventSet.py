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
from ..util import time_ago

# a set of events (a blog or repository)
class EventSet(models.Model):
  class Meta:
    app_label = 'dashboard'
  
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