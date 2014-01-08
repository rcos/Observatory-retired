from dashboard.feeds import *
from dashboard.models import *
from dashboard.views import *
from django.conf.urls import *
import foundry.views
import observatory.urls
import settings

urlpatterns = patterns('',

    # Foundry URLs
    (r'^$', foundry.views.index),
    
    (r'^', include(observatory.urls)),
)
