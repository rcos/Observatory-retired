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

from django import template
from django.template.loader import render_to_string

register = template.Library()

###
# A function that is used sort of like inherited from but not really to do stuff
# for the fields of a form.  This stuff needs to happen on each field.
#
# @param  {String}  label  -  The label for this field (to display to the user)
# @param  {String}  id    - The id of this field element
# @param  {String}  name  - The name of this field for the POST data
# @param  {Object}  form  - The Django form object so the field can see errors and data
# @param  {Anything/None}  required  - If required, this field is required
###
def field(label, id, name, form, required):
  # If we have a default value
  if name in form.data:
    value = form.data[name]
  else:
    value = None
  
  # IF we have errors on this field
  if name in form.errors:
    errors = form.errors[name]
    print "type(errors):\n"+str(type(errors))
  else:
    errors = None
    
  return {
    'label': label, 
    'id': id, 
    'name': name, 
    'required': required, 
    'value': value, 
    'errors': errors, 
  }
  

###
# This stuff needs to happen on each text field
#
# @param  {Number}  maxlength -  The max length attribute
# @param  {String}  placeholder - The placeholder text for this field    
###
def text_field(label, id, name, form, required, maxlength, placeholder):
  context = field(label, id, name, form, required)
  context['maxlength'] = maxlength
  context['placeholder'] = placeholder
  
  return context
    
###
# The driver for an input field
#
# @param  {String}  input_type  - The type of input field
###
@register.inclusion_tag('partials/input_field.html')
def input_field(label, id, name, form, required, maxlength, placeholder, input_type):
  context = text_field(label, id, name, form, required, maxlength, placeholder)
  context['input_type'] = input_type
  
  return context
  
###
# A textarea field.
#
# @param  {Number}  rows  - rows attribute of <textarea> element
# @param  {Number}  cols  - cols attribute of the <textarea> element
###
@register.inclusion_tag('partials/textarea_field.html')
def textarea_field(label, id, name, form, required, maxlength, placeholder, rows, cols):
  context = text_field(label, id, name, form, required, maxlength, placeholder)
  context['rows'] = rows
  context['cols'] = cols
  
  return context
  
###
# A select field
#
# @param  {String}  default  -  The default value for the dropdown.
###
@register.inclusion_tag('partials/select_field.html')
def select_field(label, id, name, form, required, default):
  context = field(label, id, name, form, required)
  context['default'] = default
  context['options'] = form.fields[name].choices
  return context
