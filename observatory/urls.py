from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^observatory/', include('observatory.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin', include(admin.site.urls)),
    
    # users
    (r'^register', 'dashboard.views.users.register'),
    (r'^login', 'dashboard.views.users.login'),
    (r'^logout', 'dashboard.views.users.logout'),
    (r'^users/create', 'dashboard.views.users.create'),
    (r'^users/authenticate', 'dashboard.views.users.authenticate'),
    
    # projects
    (r'^projects/add', 'dashboard.views.projects.add'),
    (r'^projects/create', 'dashboard.views.projects.create'),
    (r'^projects/modify/(\d+)', 'dashboard.views.projects.modify'),
    (r'^projects/update/(\d+)', 'dashboard.views.projects.update'),
    (r'^projects/(\d+)', 'dashboard.views.projects.show'),
    (r'^projects/list', 'dashboard.views.projects.list'),
    
    # default to showing the dashboard view (for now)
    (r'', 'dashboard.views.projects.index')
)
