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
import re
from BeautifulSoup import BeautifulSoup, Comment
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import escape
from HTMLParser import HTMLParser
from unicodedata import normalize
from urllib import urlopen

INVALID_URL_PATHS = (
  "add-user",
  "remove-user",
  "add",
  "list"
)

# Prevents duplicate queries by settings relationship properties of instances
# in a query set that point to an object that appears more than once to a
# single instance. The function assumes that property_id will be a unique
# identifier to an object of a specific type in the database.
# 
# Arguments are the query set, then an arbitrary amount of string property
# names. Keyword arguments may also provide starting dictionaries. This is
# useful when requesting users, as it avoids duplicating the logged in user.
def avoid_duplicate_queries(queryset, *properties, **defaults):
  sets = {}
  for property in properties:
    sets[property] = defaults[property] if property in defaults else {}
  
  for object in queryset:
    for property in properties:
      id = getattr(object, property + "_id")
      
      if id in sets[property]:
        setattr(object, property, sets[property][id])
      else:
        sets[property][id] = getattr(object, property)

# adds a "pages" method to paginator, which returns a list of the pages
class ListPaginator(Paginator):
  def pages(self):
    return [self.page(i) for i in range(1, self.num_pages + 1)]

# fuzzies up time spans into nice simple numbers of time units ago
def time_ago(date, time = datetime.datetime.utcnow()):
  def plural(number, descriptor):
    if number == 1:
      return "{0} {1} ago".format(number, descriptor)
    else:
      return "{0} {1}s ago".format(number, descriptor)
  
  delta = time - date
  
  if delta.seconds + delta.days * 24 * 3600 <= 0:
    return "moments ago"
  if delta.days >= 7:
    return plural(int(delta.days / 7), "week")
  if delta.days > 0:
    return plural(delta.days, "day")
  if delta.seconds >= 60 * 60:
    return plural(int(delta.seconds / (60 * 60)), "hour")
  if delta.seconds >= 60:
    return plural(int(delta.seconds / 60), "minute")
  return plural(delta.seconds, "second")

def sanitize(string, allowed_tags = None, strip_tags = None):
  js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
  
  if allowed_tags:
    allowed_tags = [tag.split(":") for tag in allowed_tags]
    allowed_tags = dict((tag[0], tag[1:]) for tag in allowed_tags)
  
  soup = BeautifulSoup(string)
  for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
    comment.extract()
  
  for tag in soup.findAll(True):
    if strip_tags and tag.name in strip_tags:
      tag.hidden = True
    else:
      if not allowed_tags or tag.name not in allowed_tags:
        tag.extract()
      else:
        tag.attrs = [(attr, js_regex.sub('', val))
                     for attr, val in tag.attrs
                     if attr in allowed_tags[tag.name]]
  return soup.renderContents().decode("utf8")

def url_pathify_safe(model, string, invalid_paths = INVALID_URL_PATHS,
                     max_length = 128):
  url_path = url_pathify(string)
  final_url_path = url_path
  
  # if the name is not unique, append a number
  suffix_num = 0
  while (len(model.objects.filter(url_path = final_url_path)) is not 0 or
         final_url_path in invalid_paths):
    suffix_num += 1
    suffix = str(suffix_num)
    while len(url_path) + len(suffix) > max_length:
      url_path = url_path[:-1]
    final_url_path = url_path + suffix
  return final_url_path

def url_pathify(string):
  # replace space with dash, lowercase, drop nonalphabeticals or numbers
  string = re.sub(r"[^1-9a-z-]", "", string.lower().replace(" ", "-"))
  
  # remove dashes from the start or the end
  #string = re.sub(r"^-|-$", "", string)
  
  # remove redundant dashes
  return re.sub(r"-+", "-", string)

def force_url_paths(view, *url_paths, **kwargs):
  pathified = [url_pathify(url_path) for url_path in url_paths]
  
  if tuple(pathified) != url_paths:
    if 'page' in kwargs:
      pathified.append(kwargs['page'])
    
    return HttpResponseRedirect(reverse(view, args = pathified))
  else:
    return None

def find_author(author_name):
  author = None
  
  # attempt to extract the email
  email = re.findall("<.*@.*\..*>", author_name)
  if len(email) == 1:
    author_name = author_name.replace(email[0], "").strip()
    author_email = email[0][1:-1]
    try:
      author = User.objects.get(email__iexact = author_email)
    except:
      author = None
  else:
    author_email = None
  
  # if the author can't be found via email address, try via name
  if author is None:
    author_firstlast = author_name.split(' ')
    if len(author_firstlast) > 1:
      authors = User.objects.filter(first_name__iexact = author_firstlast[0],
                                    last_name__iexact = author_firstlast[1])
      if len(authors) is 1:
        author = authors[0]
  
  return author, author_name, author_email

def format_diff(diff):
  if diff is None: return None
  
  last_was_minusminusminus = False
  added, removed, changed = 0, 0, 0
  
  out = ""
  for line in diff.split("\n"):
    if "\0" in line:
      continue
    
    classes = (('+++', 'added-file'),
               ('---', 'removed-file'),
               ('@@',  'file-lines'),
               ('+',   'line-added'),
               ('-',   'line-removed'))
    
    try:
      line = escape(unicode(line)).replace("\t", "  ")
      
      for item in classes:
        if line.startswith(item[0]):
          out += "<pre class='diff {0}'>{1}</pre>\n".format(item[1], line)
          
          # keep track of lines added and removed as well as files changed
          if item[0] == "-":
            removed += 1
          if item[0] == "+":
            added += 1
          
          if item[0] == "---":
            last_was_minusminusminus = True
            changed += 1
          if item[0] == "+++" and not last_was_minusminusminus:
            changed += 1
          elif last_was_minusminusminus:
            last_was_minusminusminus = False
          break
      
    except UnicodeDecodeError as e:
      continue
  return out, added, removed, changed
