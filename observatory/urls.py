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
    (r'^register', 'dashboard.users.register'),
    (r'^login', 'dashboard.users.login'),
    (r'^logout', 'dashboard.users.logout'),
    (r'^users/create', 'dashboard.users.create'),
    (r'^users/authenticate', 'dashboard.users.authenticate'),
    
    
    # projects
    (r'^projects/add', 'dashboard.views.add_project'),
    (r'^projects/create', 'dashboard.views.create_project'),
    (r'^projects/modify/(\d+)', 'dashboard.views.modify_project'),
    (r'^projects/update/(\d+)', 'dashboard.views.update_project'),
    (r'^projects/(\d+)', 'dashboard.views.show_project'),
    (r'^projects/list', 'dashboard.views.list_projects'),
    
    # default to showing the dashboard view (for now)
    (r'', 'dashboard.views.index')
)
