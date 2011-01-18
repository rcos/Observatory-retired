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

from django.db import models
from django.contrib.auth.models import User
from Project import Project

class AuthorRequest(models.Model):
  class Meta:
    app_label = 'dashboard'
  
  # the user that is requesting to be an author
  user = models.ForeignKey(User)
  
  # the project the user is requesting to be an author for
  project = models.ForeignKey(Project)
  
  # automatically detected by observatory finding a commit by the author
  autodetected = models.BooleanField(default = False)
  
  def approve(self):
    self.project.authors.add(self.user)
    self.project.save()
    self.delete()
  
  def reject(self):
    self.delete()