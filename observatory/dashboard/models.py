from django.db import models
from django.contrib.auth.models import User

# a blog for a project
class Blog(models.Model):
  url = models.URLField(max_length = 64)
  rss = models.URLField("Blog RSS Feed", max_length = 64)
  
# a post in a blog
class BlogPost(models.Model):
  # title of the post
  title = models.CharField(max_length = 128)
  
  # the text of the post
  content = models.TextField()
  summary = models.TextField()
  
  # when the post was made
  date = models.DateTimeField()
  
  # what blog the post is associated with
  blog = models.ForeignKey(Blog)
  
# a version control repository
class Repository(models.Model):
  # version control
  url = models.URLField("Source URL", max_length = 64)
  checkout = models.URLField("Source Checkout URL", max_length = 64)

# a commit in a repository
class Commit(models.Model):
  # the url to the commit (in cgit, etc.)
  url = models.URLField("Commit URL", max_length = 200)

  # the author of the commit, if he/she is in dashboard
  author = models.ForeignKey(User)

  # the author's name, if he/she isn't in dashboard
  author_name = models.CharField(max_length = 64)

  # the repository the commit is part of
  respository = models.ForeignKey(Repository)

# an RCOS project
class Project(models.Model):  
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
  wiki = models.CharField(max_length = 64)
  
  # authors of the project
  authors = models.ManyToManyField(User)
  
  # if the project is currently active
  active = models.BooleanField("Currently Active")
  
  # string representation of the project
  def __unicode__(self):
    return self.title