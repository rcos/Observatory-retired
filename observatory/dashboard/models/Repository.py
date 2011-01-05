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

from django.db import models
from lib import feedparser, dateutil
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
    import Commit
    
    if self.cloned:
      pass
    else:
      max_date = self.most_recent_date
      for commit in feedparser.parse(self.repo_rss).entries:
        date = dateutil.parser.parse(commit.date)
        try:
          date = (date - date.utcoffset()).replace(tzinfo=None)
        except:
          pass

        # find the new most recently updated date
        if max_date < date:
          max_date = date
        
        # don't re-add old commits
        if self.most_recent_date >= date:
          continue
        
        # can we find an author for this commit?
        author_name = commit.author_detail['name']
        try:
          author_firstlast = author_name.split(' ')
          authors = User.objects.filter(first_name = author_firstlast[0],
                                        last_name = author_firstlast[1])
          if len(authors) is 1:
            author = authors[0]
          else:
            author = None
        except:
          author = None
        
        # create and save the commit object
        commit = Commit.Commit(author_name = author_name,
                               title = commit.title,
                               description = commit.description,
                               url = commit.link,
                               date = date)
        commit.repository = self
        if author is not None:
          commit.author = author
        commit.save()
        
        # print out results
        print "Commit by {0} in {1} at {2}".format(author_name,
                                                   self.project.title,
                                                   date)
        
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