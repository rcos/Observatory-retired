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
import re
from colorsys import hsv_to_rgb
from django.db import models
from django.contrib.auth.models import User
from Repository import Repository
from Blog import Blog

INVALID_PROJECT_URL_PATHS = (
  "add-user",
  "remove-user",
  "add",
  "list"
)

# an open source project tracked by observatory
class Project(models.Model):
  class Meta:
    app_label = 'dashboard'
  
  # basic things
  title = models.CharField(max_length = 32)
  
  # a short description of the project
  description = models.TextField()
  
  # project's web presence
  website = models.URLField(max_length = 64)
  
  # version control
  repository = models.OneToOneField(Repository)
  
  # blog
  blog = models.OneToOneField(Blog)
  
  # wiki
  wiki = models.URLField(max_length = 64)
  
  # authors of the project
  authors = models.ManyToManyField(User)
  
  # if the project is currently active
  active = models.BooleanField("Currently Active")
  
  # the score of the project, computed after each fetch
  score = models.FloatField(blank = True, null = True)
  
  # the rank of the project, computed after each fetch
  rank = models.IntegerField(blank = True, null = True)
  
  # the url path component that points to this project
  url_path = models.CharField(max_length = 32, editable = False, null = True)
  
  # assign the url path when the project is first created
  def save(self, *args, **kwargs):
    if self.url_path is None:
      # replace space with dash, lowercase, drop nonalphabeticals
      url_path = re.sub(r"[^a-z-]", "", self.title.lower().replace(" ", "-"))
      self.url_path = url_path
      
      # if the name is not unique, append a number (this shouldn't be an issue)
      suffix_num = 0
      while (len(Project.objects.filter(url_path = self.url_path)) is not 0 or
             self.url_path in INVALID_PROJECT_URL_PATHS):
        suffix_num += 1
        suffix = str(suffix_num)
        while len(url_path) + len(suffix) > 32:
          url_path = url_path[:-1]
        self.url_path = url_path + suffix
    
    # call up to the default save
    super(Project, self).save(*args, **kwargs)
  
  # fetch and update the project's blog and repository
  def fetch(self):
    self.blog.fetch()
    self.repository.fetch()
    
    # determine the score of the project
    now = datetime.datetime.now()
    r = (now - self.repository.most_recent_date).seconds
    b = (now - self.blog.most_recent_date).seconds
    self.score = (r * r + r * b + b * b + r) / 1000000
    self.save()
  
  # string representation of the project
  def __unicode__(self):
    return self.title
  
  # CSS for background of ranking emblem
  def rank_emblem_css(self):
    # a bit inefficient?
    count = float(len(Project.objects.all()))
    hue = self.rank / count
    mainbg = hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.75)
    lightbg = hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.9)
    darkbg = hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.6)
    inset = hsv_to_rgb(0.3 - hue * 0.3, 0.5, 0.2)
    
    return """
      background:rgb({0},{1},{2});
      background-image: -webkit-gradient(linear, left bottom, left top,
        from(rgb({0},{1},{2})),
        to(rgb({9},{10},{11})));
      background-image: -moz-linear-gradient(100% 100% 90deg,
        rgb({0},{1},{2}),
        rgb({9},{10},{11})
      );
      -moz-text-shadow: 0px -1px 1px rgb({6},{7},{8});
      -webkit-text-shadow: 0px -1px 1px rgb({6},{7},{8});
      text-shadow: 0px -1px 1px rgb({6},{7},{8});
      """.format(int(mainbg[0] * 255),
                 int(mainbg[1] * 255),
                 int(mainbg[2] * 255),
                 int(darkbg[0] * 255),
                 int(darkbg[1] * 255),
                 int(darkbg[2] * 255),
                 int(inset[0] * 255),
                 int(inset[1] * 255),
                 int(inset[2] * 255),
                 int(lightbg[0] * 255),
                 int(lightbg[1] * 255),
                 int(lightbg[2] * 255))