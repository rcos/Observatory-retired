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

from django import forms
from django.contrib.auth.models import User
from dashboard.models import *

class RequiredForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(RequiredForm, self).__init__(*args, **kwargs)
    for name, field in self.fields.items():
      if not field.widget.attrs.has_key("required"):
        field.widget.attrs.update({ "required": "true" })

class ProjectForm(RequiredForm):
  class Meta:
    model = Project
    fields = ('title', 'website', 'wiki', 'description', 'active')

class RepositoryForm(RequiredForm):
  class Meta:
    model = Repository

class ClonedRepositoryForm(RequiredForm):
  class Meta:
    model = Repository
    fields = ('web_url', 'clone_url', 'vcs')

class FeedRepositoryForm(RequiredForm):
  class Meta:
    model = Repository
    fields = ('web_url', 'repo_rss', 'cmd')

class BlogForm(RequiredForm):
  class Meta:
    model = Blog
    fields = ('url', 'rss')

class BlogPostForm(forms.ModelForm):
  class Meta:
    model = BlogPost
    fields = ('title', 'markdown')

class UploadScreenshotForm(forms.Form):
  title = forms.CharField(max_length = 32)
  description = forms.CharField(max_length = 100)
  file = forms.ImageField()

class RegistrationForm(RequiredForm):
  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'password')
    widgets = { 'password': forms.PasswordInput() }

class LoginForm(RequiredForm):
  class Meta:
    model = User
    fields = ('email', 'password')
    widgets = { 'password': forms.PasswordInput() }

class ForgotPasswordForm(forms.Form):
  email = forms.EmailField()
