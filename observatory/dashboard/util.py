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

from collections import defaultdict
from hashlib import md5
from HTMLParser import HTMLParser
from urllib import urlopen

def gravatar(user, size):
  # get an md5 hash of the user (with gravatar's parameters)
  m = md5()
  m.update(user.email.strip().lower())
  hash = m.hexdigest()
  url = 'http://www.gravatar.com/avatar/{0}?d=retro&r=pg&s={1}'
  return url.format(hash, size)

def find_rss(url):
  # try to find an rss feed
  try:
    return RSSFinder().find(urlopen(url).read())
    
  # alright, this is a silent failure. is it good to show potentially complex
  # error message to the user or is it better to just say "hey, we can't find
  # your feed, can you just give it to us literally?"
  except:
    return None

# an HTMLParser subclass for locating RSS feeds in HTML files
class RSSFinder(HTMLParser):
  rss_feed = None
  
  def find(self, html):
    self.feed(html)
    self.close()
    return self.rss_feed
  
  def handle_starttag(self, tag, attrs):
    # only both with link tags (if we haven't already)
    if tag == 'link':
      link = None
      is_rss = False
      
      # iterate over the attributes
      for (name, data) in attrs:
        # if it is the link tag, set the link
        if name == 'href':
          link = data
        
        # this is an RSS tag!
        elif (data == 'application/rss+xml' or
              data == 'application/atom+xml' and
              name == 'type'):
          is_rss = True
      
      # if an RSS feed was found, set it in the outer scope
      if is_rss and data is not None:
        self.rss_feed = link