from django.forms import ModelForm
from dashboard.models import *

class ProjectForm(ModelForm):
  class Meta:
    model = Project
    fields = ('title', 'website', 'wiki', 'active', 'description')
