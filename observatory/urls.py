from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^observatory/', include('observatory.foo.urls')),
    
    (r'^dashboard/add', 'dashboard.views.add_project'),
    (r'^dashboard/create', 'dashboard.views.create_project'),
    (r'^dashboard/show/(\d+)', 'dashboard.views.show_project'),
    (r'^dashboard/modify/(\d+)', 'dashboard.views.modify_project'),
    (r'^dashboard/update/(\d+)', 'dashboard.views.update_project'),
    
    # default to showing the dashboard view (for now)
    (r'^dashboard', 'dashboard.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
