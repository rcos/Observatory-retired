from dashboard.feeds import *
from dashboard.models import *
from dashboard.views import *
from django.conf.urls.defaults import *
import rcos.views
import observatory.urls
import settings

from django.contrib import admin

urlpatterns = patterns('',
    
    # RCOS views
    (r'^donor/$', rcos.views.donor),
    (r'^students/$', rcos.views.students),
    (r'^courses/$', rcos.views.courses),
    (r'^talks/$', rcos.views.talks),
    (r'^programming-competition/$', rcos.views.progcomp),
    (r'^achievements/$', rcos.views.achievements),
    (r'^urp-application/$', rcos.views.urpapplication),
    (r'^links-and-contacts/$', rcos.views.linksandcontacts),
    (r'^irc/$', rcos.views.irc),
    (r'^calendar/$', rcos.views.calendar),
    (r'^howtojoin/$', rcos.views.howtojoin),
    (r'^past-projects/$', rcos.views.past_projects),
    (r'^$', rcos.views.index),
    
    (r'^', include(observatory.urls)),
)
