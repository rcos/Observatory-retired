#!/usr/bin/env python2

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

# Repository fetching can be very slow, so we use multiple processes for it.
# This file takes a single argument, which is the id number of a repository.

import os
import subprocess
from fetch_core import setup_environment, cprint
from shutil import rmtree
from sys import executable as python
from time import sleep

setup_environment()

from dashboard.models import Repository, Commit, Project
from observatory.settings import REPO_FETCH_TIMEOUT, REPO_FETCH_PROCESS_COUNT

CLONE_TIMEOUT = 20 * 60

class Fetcher(object):
  repo = None
  process = None
  parsing = False
  age = 0
  
  def __init__(self, repo):
    self.repo = repo
    cprint("==> Fetching {0}".format(repo.project.title),
           "yellow", attrs=["bold"])
    self.process = subprocess.Popen([python, fetch_script, str(repo.id), "&"])
  
  def second_passed(self):
    # initial clone/fetch stage
    self.process.poll()
    self.age += 1
    
    if not self.parsing:
      # time out cloning, clean up the failed clone dir, and end the fetcher
      if self.age > CLONE_TIMEOUT or self.process.returncode == 1:
        if self.process.returncode is not None:
          cprint("==> Fetching failed for {0}".format(self.repo.project.title),
                 "red", attrs=["bold"])
        else:
          cprint("==> Killing clone of {0}".format(self.repo.project.title),
                 "red", attrs=["bold"])
          self.process.terminate()

        path = os.path.dirname(os.path.abspath(__file__))
        clone_path = os.path.join(path, "..", "..", "clones",
                                  self.repo.project.url_path)
        if os.path.exists(clone_path):
          rmtree(clone_path)

        return True
      # move on to the parsing stage if fetching is complete
      elif self.process.returncode is not None:
        cprint("==> Successfully fetched {0}".format(self.repo.project.title))

        cprint("==> Parsing {0}".format(self.repo.project.title),
               "blue", attrs=["bold"])
        self.parsing = True
        self.age = 0
        self.process = subprocess.Popen([python, parse_script,
                                         str(self.repo.id)])

    else:
      # if the process finished, we're all done
      if self.process.returncode is not None:
        if not self.process.returncode:
          cprint("==> Successfully parsed {0}".format(self.repo.project.title),
                 "green", attrs=["bold"])
        return True
      
      # if the parser timed out
      if self.age > 60 * REPO_FETCH_TIMEOUT:
        # kill the parser
        cprint("==> Killing parsing of {0}".format(self.repo.project.title),
               "red", attrs=["bold"])
        self.process.terminate()
        
        # deal with the aftermath
        commits = Commit.objects.filter(repository__id = self.repo.id)
        try:
          self.repo.most_recent_date = commits.order_by("-date")[0].date
          self.repo.save()
        except IndexError:
          pass
        
        # we're (unfortunately) done
        return True
    
    return False
  
# find the parse and cleanup scripts
this_dir = os.path.abspath(os.path.dirname(__file__))
parse_script = os.path.join(this_dir, "parse_repository.py")
fetch_script = os.path.join(this_dir, "clone_or_fetch_repository.py")

# grab all repositories and put them in a list
repositories = list(Repository.objects.filter(project__active = True))

# fetch the repositories (or time out if it's concert)
fetchers = []
while True:
  # stop when all repositories have been fetched
  if len(repositories) is 0 and len(fetchers) is 0:
    break
  
  # add more fetchers if necessary
  while len(fetchers) < REPO_FETCH_PROCESS_COUNT and len(repositories) > 0:
    fetchers.append(Fetcher(repositories.pop()))
  
  # wait a second
  sleep(1)
  
  # age the fetchers, remove them if they are done
  for fetcher in fetchers:
    if fetcher.second_passed():
      project = Project.objects.get(repository__id = fetcher.repo.id)
      project.calculate_score()
      fetchers.remove(fetcher)
  
