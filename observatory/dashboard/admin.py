# enable administration of everything via the web interface
from dashboard.models import *
from django.contrib import admin

admin.site.register(Blog)
admin.site.register(BlogPost)
admin.site.register(Repository)
admin.site.register(Project)