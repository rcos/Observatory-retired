#! /usr/bin/env python2

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

# populates the database with some sample users and projects

import sys
import os
from hashlib import md5

# argv
with_svn = "--with-svn" in sys.argv

path = os.path.dirname(os.path.abspath(__file__))

# remove the database and recreate it
os.system("rm {0}/../db.sqlite".format(path))
os.system("python2 {0}/../manage.py syncdb --noinput".format(path))
os.system("python2 {0}/../manage.py migrate dashboard --noinput".format(path))
os.system("python2 {0}/../manage.py migrate dashboard --noinput".format(path))

# django setup
sys.path.insert(0, path)
sys.path.insert(0, os.path.abspath(os.path.join(path, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(path, '..', '..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'observatory.settings'

from dashboard.models import *
from django.contrib.auth.models import User
from emaillist.models import EmailAddress

# make some users
for person in [('natesm@gmail.com', 'password', 'Nate', 'Stedman'),
               ('peterhajas@gmail.com', 'password', 'Peter', 'Hajas'),
               ('hortont424@gmail.com', 'password', 'Tim', 'Horton'),
               ('arsenm2@rpi.edu', 'password', 'Matt', 'Arsenault'),
               ('doughj3@rpi.edu', 'password', 'Joseph', 'Dougherty'),
			   ('ben.shippee@gmail.com', 'password','Ben', 'Shippee'),
			   ('colin@daedrum.net', 'password','Colin', 'Rice'),
               ]:
  m = md5()
  m.update(person[0])
  user = User.objects.create_user(m.hexdigest()[0:30], person[0], person[1])
  user.first_name = person[2]
  user.last_name = person[3]
  user.is_staff = True
  user.info = UserInfo(user=user,mentor=True)
  user.info.save()
  user.is_superuser = True
  user.save()
  email = EmailAddress(address=person[0], user=user)
  email.save()
  print "Added {0}".format(user.get_full_name())
  
# make some projects
ease_blog = Blog(from_feed = False)
ease_blog.save()
ease_repo = Repository(web_url = "http://git.gnome.org/browse/ease",
                       clone_url = "git://git.gnome.org/ease",
                       from_feed = False)
ease_repo.save()
ease = Project(title = "Ease",
               description = "A presentation application for the Gnome Desktop.",
               website = "http://www.ease-project.org",
               wiki = "http://live.gnome.org/Ease",
               blog_id = ease_blog.id,
               repository_id = ease_repo.id)
ease.save()
ease.authors.add(User.objects.get(email = 'natesm@gmail.com'))
ease.save()

mnot_blog = Blog(from_feed = True,
                 url = "http://www.peterhajas.com/blog",
                 rss = "http://www.peterhajas.com/blog/atom.xml")
mnot_blog.save()
mnot_repo = Repository(web_url = "https://github.com/peterhajas/MobileNotifier",
                       clone_url = "git://github.com/peterhajas/MobileNotifier.git",
                       from_feed = False)
mnot_repo.save()
mnot = Project(title = "MobileNotifier",
               description = "iOS notifications and stuff.",
               website = "http://www.peterhajas.com",
               wiki = "http://www.peterhajas.com",
               blog_id = mnot_blog.id,
               repository_id = mnot_repo.id,
               pending = True)
mnot.save()
mnot.authors.add(User.objects.get(email = 'peterhajas@gmail.com'))
mnot.save()

obsv_blog = Blog(from_feed = True,
                 url = "http://www.natestedman.com",
                 rss = "http://www.natestedman.com/feed")
obsv_blog.save()
obsv_repo = Repository(web_url = "https://github.com/rcos/Observatory",
                       clone_url = "git://github.com/rcos/Observatory.git",
                       cmd = "git clone",
                       from_feed = False)
obsv_repo.save()
obsv = Project(title = "Observatory",
               description = "A Python (Django) based dashboard for the Rensselaer Center for Open Source Software.",
               website = "http://nate.xen.prgmr.com",
               wiki = "http://nate.xen.prgmr.com",
               blog_id = obsv_blog.id,
               repository_id = obsv_repo.id)
obsv.save()
obsv.authors.add(User.objects.get(email = 'natesm@gmail.com'))
obsv.authors.add(User.objects.get(email = 'hortont424@gmail.com'))
obsv.authors.add(User.objects.get(email = 'peterhajas@gmail.com'))
obsv.authors.add(User.objects.get(email = 'arsenm2@rpi.edu'))
obsv.authors.add(User.objects.get(email = 'colin@daedrum.net'))
obsv.save()

note_blog = Blog(from_feed = True,
                 url = "http://hortont.com/blog",
                 rss = "http://www.hortont.com/blog//feed/rss.xml")
note_blog.save()
note_repo = Repository(web_url = "https://github.com/hortont424/Notebook",
                       clone_url = "git://github.com/hortont424/notebook.git",
                       cmd = "git clone",
                       from_feed = False)
note_repo.save()
note = Project(title = "Notebook",
               description = "Mathematica? In my Python?",
               website = "http://hortont.com",
               wiki = "http://hortont.com",
               blog_id = note_blog.id,
               repository_id = note_repo.id)
note.save()
note.authors.add(User.objects.get(email = 'hortont424@gmail.com'))
note.authors.add(User.objects.get(email = 'arsenm2@rpi.edu'))
note.save()

milk_blog = Blog(from_feed = True,
                 url = "http://whatmannerofburgeristhis.com/blog",
                 rss = "http://www.whatmannerofburgeristhis.com/blog//feed/rss.xml")
milk_blog.save()
milk_repo = Repository(web_url = "https://github.com/Milkyway-at-home/milkywayathome_client",
                       repo_rss = "https://github.com/Milkyway-at-home/milkywayathome_client/commits/master.atom",
                       cmd = "git clone",
                       from_feed = True)
milk_repo.save()
milk = Project(title = "milkyway@home",
               description = "Doing science.",
               website = "http://whatmannerofburgeristhis.com",
               wiki = "http://whatmannerofburgeristhis.com",
               blog_id = milk_blog.id,
               repository_id = milk_repo.id,
               mentor = User.objects.filter(last_name = "Rice")[0])
milk.save()
milk.authors.add(User.objects.get(email = 'arsenm2@rpi.edu'))
milk.save()

if with_svn:
  awav_blog = Blog(from_feed = False)
  awav_blog.save()
  awav_repo = Repository(web_url = "http://code.google.com/p/awesome-wav/",
                         clone_url = "http://awesome-wav.googlecode.com/svn/trunk/",
                         vcs = "svn",
                         cmd = "git clone",
                         from_feed = False)
  awav_repo.save()
  awav = Project(title = "awesome-wav",
                 description = """The awesome-wav project is a project designed to encode any data file into a PCM or IEEE float WAV audio file and be virtually undetectable. The potential uses for this project are many and varied. It is a command-line only, cross-platform program.

                 This project is currently in development and, though functional, is not guaranteed to work properly under all conditions.

                 The program currently supports 8, 16, 24, and 32 bit PCM WAV files, 32 and 64 bit IEEE float WAV files, and supports compressing the input data using zlib or quicklz. It also supports data encryption (AES ECB).""",
                 website = "http://code.google.com/p/awesome-wav/",
                 wiki = "http://code.google.com/p/awesome-wav/",
                 blog_id = awav_blog.id,
                 repository_id = awav_repo.id)
  awav.save()


cnct_blog = Blog(url = "http://blog.concertsoundorganizer.com",
                 rss = "http://blog.concertsoundorganizer.com/rss")
cnct_blog.save()
cnct_repo = Repository(web_url = "https://github.com/joshelser/Concert/",
                       clone_url = "https://github.com/joshelser/Concert.git",
                       vcs = "git",
                       from_feed = False)
cnct_repo.save()
cnct = Project(title = "Concert",
               description = """Concert is a web-based application for collaboratively organizing audio. It enables a group of musicians to upload recordings of small ideas or entire practices, and then remotely categorize and discuss these segments so that the ideas are already well-formed before the musicians actually discuss them in person.

			It is built on Django using the python-audio-tools library, as well as other dependencies.

			The software is currently not in a release state, as it is being completely re-written. You can read about the development progress here: blog.concertsoundorganizer.com""",
               website = "http://concertsoundorganizer.com/",
               wiki = "https://github.com/joshelser/Concert/wiki",
               blog_id = cnct_blog.id,
               repository_id = cnct_repo.id)
cnct.save()

if with_svn:
  fire_blog = Blog(url = "http://firedepartmentsolutions.com/",
                   rss = "http://firedepartmentsolutions.com/?q=rss.xml",
                   from_feed = True)
  fire_blog.save()
  fire_repo = Repository(web_url = "http://firedepartmentsolutions.com/websvn/listing.php?repname=Fire+Department+Management+System",
                         clone_url = "http://firedepartmentsolutions.com/svn/fdms/",
                         vcs = "svn",
                         from_feed = False)
  fire_repo.save()
  fire = Project(title = "Fire Department Management System",
                 description = "By their very nature, fire departments must record and track a large variety of data. Clean and thorough record keeping is imperative to ensure safe and proper action in the conditions under which fire departments operate. This paperwork can quickly become unmanageable, time consuming, and stressful. Time that could be better spent in training is put into clerical work, and this is not acceptable.",
                 website = "http://firedepartmentsolutions.com/",
                 wiki = "http://firedepartmentsolutions.com/",
                 blog_id = fire_blog.id,
                 repository_id = fire_repo.id)
  fire.save()

# add a bunch of dummy users to observatory to test multirow authors
for i in range(1, 20):
  user = User.objects.create_user("test{0}@something.com".format(i),
                                  "test{0}@something.com".format(i),
                                  "password")
  user.first_name = "Test"
  user.last_name = "User{0}".format(i)
  user.info = UserInfo(user=user, mentor=False)
  user.info.save()
  user.save()
  obsv.authors.add(user)
