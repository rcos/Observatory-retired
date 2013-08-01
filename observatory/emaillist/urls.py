
from django.conf.urls import *

urlpatterns = patterns('',
    url(r'remove/(\S+)$', 'emaillist.views.remove_email')
)
