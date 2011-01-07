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

import os
import settings
import subprocess
from dashboard.util import find_author, format_diff
from django.db import models
from lib import feedparser, dateutil, pyvcs
from EventSet import EventSet

# a version control repository
class Repository(EventSet):
  class Meta:
    app_label = 'dashboard'
  
  # web access to the repository
  web_url = models.URLField("Repository Web Address", max_length = 128)
  
  # cloned repository fields
  clone_url = models.CharField("Repository Clone Address", max_length = 128)
  vcs = models.CharField("Version Control System", max_length = 3,
                         default = 'git',
                         choices = (('git', 'git'),
                                    ('svn', 'Subversion'),
                                    ('hg',  'Mercurial'),
                                    ('bzr', 'Bazaar')))
  
  # non-cloned repository fields
  repo_rss = models.URLField("Repository RSS Feed", max_length = 128)
  cmd = models.CharField("Clone Command", max_length = 128)
  
  # whether the repo uses cloning or just an rss feed
  cloned = models.BooleanField()
  
  def fetch(self):
    def add_commit(title, description, author_name, date, max_date,
                   link = None, diff = None):
      # find the new most recently updated date
      if max_date < date:
        max_date = date

      # don't re-add old commits
      if self.most_recent_date >= date:
        return
        
      # can we find an author for this commit?
      # TODO: this seems incredibly presumptive of name format
      author, author_name = find_author(author_name)

      # create and save the commit object
      import Commit
      commit = Commit.Commit(author_name = author_name,
                             title = title,
                             description = description,
                             url = link,
                             diff = format_diff(diff),
                             date = date)
      commit.repository = self
      if author is not None:
        commit.author = author
      commit.save()

      # print out results
      print "Commit by {0} in {1} at {2}".format(author_name,
                                                 self.project.title,
                                                 date)

      return max_date
    
    max_date = self.most_recent_date

    if self.cloned:
      # this is a cloned repository
      fresh_clone = True

      # ensure that REPO_ROOT already exists
      try:
        os.makedirs(settings.REPO_ROOT, 0770)
      except OSError as e:
        pass
      
      # construct the name of the directory into which to clone the repository
      dest_dir = os.path.join(settings.REPO_ROOT, self.project.url_path)

      # check if we've already cloned this project
      if os.path.isdir(dest_dir):
        fresh_clone = False

      # clone the repository, or update our copy
      clone_repo_function(self.vcs)(self.clone_url, dest_dir, fresh_clone)

      # add the commits
      backend = pyvcs.backends.get_backend(self.vcs)
      repository = backend.Repository(dest_dir)

      # inspect the last five days of commits
      for commit in repository.get_recent_commits():
        date = commit.time
        try:
          date = (date - date.utcoffset()).replace(tzinfo=None)
        except:
          pass
        
        # extract the first line for the title of the commit
        try:
          commit_title = commit.message.split("\n")[0]
        except:
          commit_title = commit.message
        
        new_max_date = add_commit(commit_title, commit.message,
                                  commit.author, date, max_date,
                                  diff = commit.diff)

        if new_max_date:
          max_date = new_max_date
    else:
      # this is a feed-driven repository
      for commit in feedparser.parse(self.repo_rss).entries:
        date = dateutil.parser.parse(commit.date)
        try:
          date = (date - date.utcoffset()).replace(tzinfo=None)
        except:
          pass
        
        new_max_date = add_commit(commit.title, commit.description,
                                  commit.author_detail['name'], date, max_date,
                                  link = commit.link)

        if new_max_date:
          max_date = new_max_date
        
    self.most_recent_date = max_date
    self.save()
  
  def clone_cmd(self):
    if self.cloned:
      cmds = { 'git': 'clone', 'svn': 'co', 'hg': 'clone', 'bzr': 'branch' }
      return '{0} {1} {2}'.format(self.vcs, cmds[self.vcs], self.clone_url)
    else:
      return self.cmd

  def __unicode__(self):
    return self.web_url

def clone_git_repo(clone_url, destination_dir, fresh_clone = False):
  if fresh_clone:
    clone_cmdline = ["git", "clone", "--mirror", "--bare",
                     clone_url, destination_dir]
  else:
    clone_cmdline = ["git", "--git-dir", destination_dir, "fetch"]

  clone_subprocess = subprocess.Popen(clone_cmdline)

  if clone_subprocess.wait() != 0:
    # TODO: handle this better
    print "failed to clone from {0}".format(clone_url)

  # do something with the repos

def clone_repo_function(vcs):
  clone_repo_functions = { 'git': clone_git_repo }

  if not vcs in clone_repo_functions:
    print "don't know how to clone {0}".format(vcs)
    return None

  return clone_repo_functions[vcs]