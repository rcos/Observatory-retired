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

# Contributors are automatically added to a project when a commit by them is
# found. They can either be associated with a User or simply have a string
# name. When a User is added to a project's authors, it will no longer be
# displayed as a contributor, but it will remain stored as one in case the
# author status is removed.
class Contributor(models.Model):
  class Meta:
    app_label = 'dashboard'
  
  # the project the person contributed to
  projects = models.ManyToManyField(Project)
  
  # the person's user model or name/email
  user = models.ForeignKey(User, blank = True, null = True)
  name = models.CharField(max_length = 64, blank = True, null = True)
  email = models.CharField(max_length = 64, blank = True, null = True)
