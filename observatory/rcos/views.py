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

from dashboard.models import Project
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
  projects = Project.objects.order_by("score")[0:3]

  return render_to_response('rcos/index.html', {
      'disable_content': True,
      'projects': projects
    }, context_instance = RequestContext(request))

def donor(request):
  return render_to_response('rcos/donor.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))

def students(request):
  return render_to_response('rcos/students.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))

def courses(request):
  return HttpResponseRedirect("http://public.kitware.com/"
                              "OpenSourceSoftwarePractice/index.php/"
                              "Fall2010/Main_Page")

def talks(request):
  return render_to_response('rcos/talks.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))

def progcomp(request):
  return render_to_response('rcos/progcomp.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))

def achievements(request):
  return render_to_response('rcos/achievements.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))

def urpapplication(request):
  return HttpResponseRedirect("http://rcos.rpi.edu/URP_Application.pdf")

def linksandcontacts(request):
  return render_to_response('rcos/linksandcontacts.html', {
      'disable_content': True
    }, context_instance = RequestContext(request))

def irc(request):
  return HttpResponseRedirect("http://webchat.freenode.net/?channels=#rcos")
