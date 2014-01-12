from dashboard.feeds import *
from dashboard.models import *
from dashboard.views import *
from django.conf.urls import *
import foundry.views
import observatory.urls
import observatory.settings

urlpatterns = patterns('',

    # Foundry URLs
    (r'^$', foundry.views.index),
    (r'^foundry/mokr$', foundry.views.mokr),
    
    (r'^', include(observatory.urls)),
)


if observatory.settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': observatory.settings.MEDIA_ROOT}))