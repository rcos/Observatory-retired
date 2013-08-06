from dashboard.feeds import *
from dashboard.views import *
from django.conf.urls import *

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^observatory/', include('observatory.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #dashboard
    (r'^', include('dashboard.urls')),

	#tasks
	(r'^todo/', include('todo.urls')),

	#email
	(r'^email/', include('emaillist.urls')),

    # feed
    (r'^event/([^\.]*)/$', feed.event),
    (r'^feed/$', feed.feed),
    (r'^feed\.rss$', EventsFeed()),

)

