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
import os
import random
from colorsys import hsv_to_rgb
from django.db import models
from django.contrib.auth.models import User
from settings import GREEN_SCORE, RED_SCORE, UNCERTAIN_SCORE, UNHAPPY_SCORE
from settings import MEDIA_URL, MAX_SCORE_MINUTES
from dashboard.util import url_pathify_safe
from Repository import Repository
from Blog import Blog
from URLPathedModel import URLPathedModel

random.seed()

# an open source project tracked by observatory
class Project(URLPathedModel):
  class Meta:
    app_label = 'dashboard'
  
  # basic things
  title = models.CharField(max_length = 200)
  
  # a short description of the project
  description = models.TextField()
  
  # project's web presence
  website = models.URLField(max_length = 200)
  
  # version control
  repository = models.OneToOneField(Repository)
  
  # blog
  blog = models.OneToOneField(Blog)
  
  # wiki
  wiki = models.URLField(max_length = 200)
  
  # authors of the project
  authors = models.ManyToManyField(User)
  
  # if the project is currently active
  active = models.BooleanField("Currently Active")
  
  # the score of the project, computed after each fetch
  score = models.IntegerField(blank = True, null = True)
  
  # the number of presentations the group has made this semester
  presentations = models.IntegerField(default = 0)
  
  # assign the url path when the project is first created
  def save(self, *args, **kwargs):
    # clip max lengths
    self.title = self.title[0:200]
    self.website = self.website[0:200]
    self.wiki = self.wiki[0:200]
    
    # call up to the default save
    super(Project, self).save(*args, **kwargs)
  
  # fetch and update the project's blog and repository
  def fetch(self):
    self.blog.fetch()
    self.repository.fetch()
    self.calculate_score()
  
  # determine the score of the project
  def calculate_score(self):
    now = datetime.datetime.utcnow()
    if self.repository.most_recent_date != datetime.datetime(1, 1, 1):
      td = (now - self.repository.most_recent_date)
      r = (td.seconds + td.days * 24 * 3600) / 60
    else:
      r = MAX_SCORE_MINUTES
    r = min([r, MAX_SCORE_MINUTES])
    
    if self.blog.most_recent_date != datetime.datetime(1, 1, 1):
      td = (now - self.blog.most_recent_date)
      b = (td.seconds + td.days * 24 * 3600) / 60
    else:
      b = MAX_SCORE_MINUTES
    b = min([b, MAX_SCORE_MINUTES])
    
    self.score = r * 1.5 + b
    self.save()
  
  # string representation of the project
  def __unicode__(self):
    return self.title
  
  # face image for scoring emblem
  def score_emblem_face(self):
    if self.score < UNCERTAIN_SCORE:
      return os.path.join(MEDIA_URL, "pixels", "face-happy.png")
    elif self.score < UNHAPPY_SCORE:
      return os.path.join(MEDIA_URL, "pixels", "face-uncertain.png")
    return os.path.join(MEDIA_URL, "pixels", "face-unhappy.png")
  
  # CSS for background of scoring emblem
  def score_emblem_css(self):
    hue = min([1, max(0, float(self.score - GREEN_SCORE) /
                               (RED_SCORE - GREEN_SCORE))])
    
    mainbg = hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.75)
    lightbg = hsv_to_rgb(0.3 - hue * 0.3, 0.9, 0.9)
    
    return """
      background:rgb({0},{1},{2});
      background-image: -webkit-gradient(linear, left bottom, left top,
        from(rgb({0},{1},{2})),
        to(rgb({3},{4},{5})));
      background-image: -moz-linear-gradient(100% 100% 90deg,
        rgb({0},{1},{2}),
        rgb({3},{4},{5})
      );
      """.format(int(mainbg[0] * 255),
                 int(mainbg[1] * 255),
                 int(mainbg[2] * 255),
                 int(lightbg[0] * 255),
                 int(lightbg[1] * 255),
                 int(lightbg[2] * 255))
  
  def random_main_page_screenshot(self):
    from Screenshot import Screenshot
    screens = Screenshot.objects.filter(project = self)
    
    if len(screens) is 0:
      return None

    return screens[random.randint(0, len(screens) - 1)].main_page_url()
