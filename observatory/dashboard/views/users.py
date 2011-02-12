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

from dashboard.forms import LoginForm, RegistrationForm, ForgotPasswordForm
from dashboard.models import Contributor, Event
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from hashlib import md5
from observatory.dashboard.views import projects
from observatory.settings import RECAPTCHA_PUBLIC, RECAPTCHA_PRIVATE
from observatory.lib.recaptcha.client import captcha

# display's the user's profile
def profile(request, user_id):
  user = get_object_or_404(User, id = user_id)
  try:
    contributor = Contributor.objects.get(user = user)
  except:
    contributor = None
  
  try:
    is_self = user.id == request.user.id
  except:
    is_self = False
  
  return render_to_response('users/profile.html', {
      'user_page': user,
      'contributor': contributor,
      'is_self': is_self
    }, context_instance = RequestContext(request))

# displays both the login and registration forms. If there is an error with the
# selected form, the user is redirected to a page with only that form.
def login_or_reg(request):
  next = reverse(projects.list)
  
  if 'next' in request.GET:
    next = request.GET['next']
  
  reg_form = RegistrationForm(auto_id = "id_login_%s")
  login_form = LoginForm(auto_id = "id_login_%s")
  
  return render_to_response('users/login-register.html', {
      'next': next,
      'js_page_id': 'login-register',
      'reg_form': reg_form,
      'login_form': login_form,
      'RECAPTCHA_PUBLIC': RECAPTCHA_PUBLIC,
      'RECAPTCHA_PRIVATE': RECAPTCHA_PRIVATE
    }, context_instance = RequestContext(request))

# displays a registration form
def register(request):
  if request.method == "POST":
    class RegisterError:
      pass
    
    try:
      form = RegistrationForm(request.POST)
      if not form.is_valid():
        error_header = "That's not quite right."
        raise RegisterError()
      
      if len(User.objects.filter(email = form.cleaned_data["email"])) is not 0:
        error_header = "That email is already registered."
        raise RegisterError()
      
      if form.cleaned_data['password'] != request.POST['password_confirm']:
        error_header = "Your passwords didn't match."
        raise RegisterError()
      
      # validate the captcha is recaptcha is enabled
      if RECAPTCHA_PUBLIC is not None:
        capt = captcha.submit(request.POST["recaptcha_challenge_field"],
                              request.POST["recaptcha_response_field"],
                              RECAPTCHA_PRIVATE,
                              request.META["REMOTE_ADDR"])
        if not capt.is_valid:
          error_header = "Let's try that captcha again."
          raise RegisterError()
      
      resp = create_user(request, form)
      return resp
    except RegisterError:
      pass
  
  # GET
  else:
    error_header = None
    form = RegistrationForm()
  
  return render_to_response('users/register.html', {
      'next': reverse(projects.list),
      'reg_form': form,
      'error_header': error_header,
      'RECAPTCHA_PUBLIC': RECAPTCHA_PUBLIC,
      'RECAPTCHA_PRIVATE': RECAPTCHA_PRIVATE
    }, context_instance = RequestContext(request))
  
# creates a user, submitted from register
def create_user(request, form):
  data = form.cleaned_data
  
  # use an md5 of the email as a username
  m = md5()
  m.update(data["email"])

  # if it's ok, register the user
  user = User.objects.create_user(m.hexdigest()[0:30],
                                  data['email'],
                                  data['password'])
  
  # set the user's first/last names
  user.first_name = data['first_name']
  user.last_name = data['last_name']
  
  # save the user
  user.save()
  
  # search past events for the user's email
  for event in Event.objects.filter(author_email__iexact = user.email,
                                    author = None):
    event.author = user
    event.save()
  
  # search past events for the user's first and last name
  name = user.get_full_name()
  for event in Event.objects.filter(author_name__iexact = name, author = None):
    event.author = user
    event.save()
  
  # search contributors for the user's name and email
  for contrib in Contributor.objects.filter(email__iexact = user.email,
                                            user = None):
    contrib.user = user
    contrib.save()
  
  for contrib in Contributor.objects.filter(name__iexact = name, user = None):
    contrib.user = user
    contrib.save()
  
  # log the user in (since we can't send emails for validation AFAIK)
  user = auth.authenticate(username = user.username,
                           password = data['password'])
  auth.login(request, user)
  
  return HttpResponseRedirect(request.POST['next'])

# allows a user to login
def login(request):
  next = reverse(projects.list)
  
  if request.method == 'POST':
    if 'next' in request.POST:
      next = request.POST['next']
      
    login_form = LoginForm(request.POST, auto_id = "id_login_%s")
    if login_form.is_valid():
      try:
        data = login_form.cleaned_data
        
        # query for a user via email
        user = User.objects.get(email = data['email'])
        
        # authenticate that user
        user = auth.authenticate(username = user.username,
                                 password = data['password'])
        
        # if the password is incorrect, redireect to the login page
        if user is None:
          return HttpResponseRedirect(reverse(login))
        
        # otherwise, log the user in
        if user.is_active:
          auth.login(request, user)
        
        return HttpResponseRedirect(next)
      except:
        raise
  else:
    login_form = LoginForm(auto_id = "id_login_%s")
  
  return render_to_response('users/login.html', {
      'next': next,
      'error_header': "Something isn't quite right.",
      'login_form': login_form
    }, context_instance = RequestContext(request))

# logs out a user
def logout(request):
  auth.logout(request)
  return HttpResponseRedirect(reverse(projects.list)) 
  
# forgot password
def forgot_password(request):
  
  forgot_password_form = ForgotPasswordForm(request.POST, auto_id="id_%s")
  if request.method == 'POST':
    if forgot_password_form.is_valid():
      try:
        data = login_form.cleaned_data
        
        # query for a user via email
        user = User.objects.get(email = data['email'])
        
        return render_to_response('users/forgot_password_success.html', {
        })
      except:
        raise Exception('An error occurred')
  else:
    forgot_password_form = ForgotPasswordForm(auto_id="id_%s")
    
    return render_to_response('users/forgot_password.html', {
      'forgot_password_form': forgot_password_form
    }, context_instance = RequestContext(request))
