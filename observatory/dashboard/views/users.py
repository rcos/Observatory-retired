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

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

# display's the user's profile
def profile(request, user_id):
  return render_to_response('users/profile.html', {
      'user_page': get_object_or_404(User, id = int(user_id))
    })

# displays both the login and registration forms. If there is an error with the
# selected form, the user is redirected to a page with only that form.
def login_or_reg(request):
  next = reverse('dashboard.views.projects.index')
  
  if 'next' in request.GET:
    next = request.GET['next']
  
  return render_to_response('users/login-register.html', {
      'next': next
    }, context_instance = RequestContext(request))

# displays a registration form
def register(request):
  return render_to_response('users/register.html', {
      'next': reverse('dashboard.views.projects.index'),
      'error_header': "Something isn't quite right."
    }, context_instance = RequestContext(request))
  
# creates a user, submitted from register
def create(request):
  # check that the passwords match
  if request.POST['password'] != request.POST['password_confirm']:
    return HttpResponseRedirect(reverse('dashboard.views.users.register'))
  
  # if it's ok, register the user
  user = User.objects.create_user(request.POST['email'],
                                  request.POST['email'],
                                  request.POST['password'])
  
  # set the user's first/last names
  user.first_name = request.POST['first']
  user.last_name = request.POST['last']
  
  # save the user
  user.save()
  
  return HttpResponseRedirect(request.POST['next'])

# allows a user to login
def login(request):
  next = reverse('dashboard.views.projects.index')
  
  if 'next' in request.GET:
    next = request.GET['next']
  
  return render_to_response('users/login.html', {
      'next': next,
      'error_header': "Something isn't quite right."
    }, context_instance = RequestContext(request))

# logins in a user, submitted from login
def authenticate(request):
  user = auth.authenticate(username = request.POST['email'],
                           password = request.POST['password'])
  
  # if the password is incorrect, redireect to the login page
  if user is None:
    return HttpResponseRedirect(reverse('dashboard.views.users.login'))
  
  # otherwise, log the user in
  if user.is_active:
    auth.login(request, user)
  
  # redirect to the root dashboard
  return HttpResponseRedirect(request.POST['next']) 

# logs out a user
def logout(request):
  auth.logout(request)
  return HttpResponseRedirect(reverse('dashboard.views.projects.index')) 
