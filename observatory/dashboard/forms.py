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

from django import forms
from dashboard.models import *

class ProjectForm(forms.ModelForm):
  class Meta:
    model = Project
    fields = ('title', 'website', 'wiki', 'active', 'description')

class RepositoryForm(forms.ModelForm):
  class Meta:
    model = Repository

class BlogForm(forms.ModelForm):
  class Meta:
    model = Blog

class UploadScreenshotForm(forms.Form):
  title = forms.CharField(max_length = 32)
  description = forms.CharField(max_length = 100)
  file = forms.ImageField()
