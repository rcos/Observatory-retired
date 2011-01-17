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

from django import template
from hashlib import md5

register = template.Library()

# gets a gravatar for a user at the specified size
def gravatar(user, size):
  return gravatar_real(user.email, size)

def contributor_gravatar(contributor, size):
  if contributor.user:
    return gravatar_real(user.email, size)
  elif contributor.email:
    return gravatar_real(contributor.email, size)
  else:
    return gravatar_real(contributor.name, size)

def gravatar_real(email, size):
  m = md5()
  m.update(email.strip().lower())
  hash = m.hexdigest()
  url = 'http://www.gravatar.com/avatar/{0}?d=retro&r=pg&s={1}'
  return url.format(hash, size)

register.filter(gravatar)
register.filter(contributor_gravatar)
