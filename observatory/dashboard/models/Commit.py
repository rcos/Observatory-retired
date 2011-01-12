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

from django.core.urlresolvers import reverse
from django.db import models
from Event import Event
from Repository import Repository

# a commit in a repository
class Commit(Event):
  class Meta:
    app_label = 'dashboard'
  
  # the url to the commit (in cgit, etc.)
  url = models.URLField("Commit URL", max_length = 200,
                        blank = True, null = True)
  
  # the diff for the commit. This won't exist for RSS commits
  diff = models.TextField(blank = True, null = True)

  # the repository the commit is part of
  repository = models.ForeignKey(Repository)
  
  def autoescape(self):
    return False
    
  def wrap_tags(self):
    if self.description.find('<pre>') is -1 and self.external:
      return ['pre']
    else:
      return None
  
  def wrap_tags_rev(self):
    tags = self.wrap_tags()
    tags.reverse()
    return tags
  
  def link(self):
    return reverse("dashboard.views.commits.show",
                   args = (self.repository.project.url_path, self.url_path))