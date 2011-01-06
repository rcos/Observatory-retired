from django import template
from django.template.loader import render_to_string

register = template.Library()


###
#   An inclusion tag for an input field on the UI.
#
#   @param  {Object}  data  - The POST data for the form, keys are 'name' attributes
#     of input elements.
###
@register.inclusion_tag('partials/input_field.html')
def input_field(label, id, input_type, name, maxlength, data, required, placeholder=None):
  
  if name in data:
    value = data[name]
  else:
    value = None
  
  return {
    'label': label, 
    'id': id,
    'input_type': input_type,  
    'name': name,
    'maxlength': maxlength, 
    'value': value, 
    'required': required, 
    'placeholder': placeholder, 
  }