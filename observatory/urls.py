from dashboard.models import *
from django.conf.urls.defaults import *
import settings

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
    
    # author requests
    (r'^author-request/approve/(\d+)',
      'dashboard.views.author_requests.approve'),
    (r'^author-request/reject/(\d+)',
      'dashboard.views.author_requests.reject'),
    
    # blog posts
    (r'^posts/add/(\d+)', 'dashboard.views.blogs.write_post'),
    (r'^posts/create/(\d+)', 'dashboard.views.blogs.create_post'),
    (r'^posts/page/(\d+)', 'dashboard.views.blogs.posts_page'),
    (r'^post/(.*)/modify', 'dashboard.views.blogs.edit_post'),
    (r'^post/(.*)/update', 'dashboard.views.blogs.update_post'),
    (r'^post/(.*)/delete', 'dashboard.views.blogs.delete_post'),
    (r'^post/(.*)', 'dashboard.views.blogs.show_post'),
    (r'^posts', 'dashboard.views.blogs.posts'),
    
    # users
    (r'^register-or-login', 'dashboard.views.users.login_or_reg'),
    (r'^register', 'dashboard.views.users.register'),
    (r'^login', 'dashboard.views.users.login'),
    (r'^logout', 'dashboard.views.users.logout'),
    (r'^user/create', 'dashboard.views.users.create'),
    (r'^user/authenticate', 'dashboard.views.users.authenticate'),
    (r'^user/(\d+)', 'dashboard.views.users.profile'),
    
    # commits
    (r'^projects/(.*)/commit/(.*)', 'dashboard.views.commits.show'),
    
    # projects
    (r'^projects/add-user', 'dashboard.views.projects.add_user'),
    (r'^projects/remove-user', 'dashboard.views.projects.remove_user'),
    (r'^projects/add', 'dashboard.views.projects.add'),
    (r'^projects/list', 'dashboard.views.projects.list'),
    (r'^projects/(.*)/upload-screenshot',
      'dashboard.views.projects.upload_screenshot'),
    (r'^projects/(.*)/modify/(\d+)', 'dashboard.views.projects.modify'),
    (r'^projects/(.*)/modify', 'dashboard.views.projects.modify'),
    (r'^projects/(.*)/blog', 'dashboard.views.blogs.show_blog'),
    (r'^projects/(.*)', 'dashboard.views.projects.show'),
    (r'^projects', 'dashboard.views.projects.index'),
    
    # serve media (for now)
    (r'^site-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    
    (r'', 'dashboard.views.main.index'),
)
