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

import calendar
import datetime
import time
from django.db import models
from dashboard.util import find_author, time_ago, sanitize

# a set of events (a blog or repository)
class EventSet(models.Model):
  class Meta:
    app_label = 'dashboard'
  
  # most recent time to add new events for
  most_recent_date = models.DateTimeField(default = datetime.datetime(1, 1, 1))
  
  # whether the event set's source is from a feed
  from_feed = models.BooleanField()
  
  # how recent was the last update?
  def age_ago(self, time = datetime.datetime.utcnow()):
    return time_ago(self.most_recent_date, time)
  
  # when was this eventset last updated?
  def when_updated(self):
    if self.most_recent_date != datetime.datetime(1, 1, 1):
      return "{0} updated {1}".format(self.__class__.__name__, self.age_ago())
    else:
      return "{0} never updated".format(self.__class__.__name__,
                                        self.age_ago())
  
  def add_event(self, klass,
                title = None,
                summary = None,
                date = None,
                author_name = None,
                from_feed = None,
                append_unsanitized = "",
                extra_args = {}):
    # convert to UTC
    secs = time.mktime(date.timetuple())
    date = datetime.datetime.utcfromtimestamp(secs)
    
    # don't re-add old events
    if self.most_recent_date >= date:
      return
    
    # can we find an author for this event?
    from dashboard.models import Blog
    if self.__class__ is not Blog or self.user is None:
      if author_name is not None:
        author, author_name, author_email = find_author(author_name)
      else:
        author = None
        author_email = None
    else:
      author = self.user
      author_email = None
    
    # sanitize the summary
    summary = append_unsanitized + sanitize(summary, [
      "h1", "h2", "h3", "h4", "h5", "h6",
      "a:href", "p", "ul", "ol", "li", "br",
      "b", "i", "u", "strong", "em", "div",
      "pre", "tt", "code"
    ])

    # create and save the event object
    event = klass(author_name = author_name,
                  title = title,
                  summary = summary,
                  from_feed = from_feed,
                  date = date,
                  author_email = author_email,
                  **extra_args)
    if author is not None:
      event.author = author
    event.save()
    
    # if this is a personal blog, we're all done
    if self.__class__ == Blog:
      if self.user is not None:
        print "Personal blog found by {0}".format(self.user.get_full_name())
        return event
    
    # set the project
    event.project = self.project
    event.save()
    
    # add a contributor for the author if they are not a project author
    if author is not None or author_name is not None:
      from Contributor import Contributor
      cont = None
      
      # if there is no "author", create a contributor associated with a
      # name and an email. this can be upgraded to a User if that person
      # joins observatory.
      if author is None:
        try:
          if author_email is not None:
            cont = Contributor.objects.get(email = author_email)
          else:
            raise Contributor.DoesNotExist()
        except Contributor.DoesNotExist:
          try:
            cont = Contributor.objects.get(name = author_name)
          except Contributor.DoesNotExist:
            cont = Contributor(name = author_name, email = author_email)
      
      # otherwise, associate with the user model
      else:
        try:
          cont = Contributor.objects.get(user = author)
        except Contributor.DoesNotExist:
          cont = Contributor(user = author)
      
      # save the contributor and add it to the project
      cont.save()
      cont.projects.add(event.project)
      
    # print out results
    print "{0} by {1}{2} in {3} at {4}".format(
      klass.__name__,
      author_name,
      " (found)" if author != None else "",
      self.project.title,
      date
    )
    return event
  
  class Meta:
    abstract = True

