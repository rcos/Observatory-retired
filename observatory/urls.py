from dashboard.models import *
from dashboard.views import *
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
    (r'^author-request/approve/(\d+)$', author_requests.approve),
    (r'^author-request/reject/(\d+)$', author_requests.reject),
    
    # blog posts
    (r'^posts/add/(\d+)$', blogs.write_post),
    (r'^posts/create/(\d+)$', blogs.create_post),
    (r'^posts/page/(\d+)$', blogs.posts_page),
    (r'^project/(.*)/post/(.*)/modify$', blogs.edit_post),
    (r'^project/(.*)/post/(.*)/update$', blogs.update_post),
    (r'^project/(.*)/post/(.*)/delete$', blogs.delete_post),
    (r'^project/(.*)/post/(.*)$', blogs.show_post),
    (r'^posts$', blogs.posts),
    
    # users
    (r'^register-or-login$', users.login_or_reg),
    (r'^register$', users.register),
    (r'^login$', users.login),
    (r'^logout$', users.logout),
    (r'^user/create$', users.create),
    (r'^user/authenticate$', users.authenticate),
    (r'^user/(\d+)$', users.profile),
    
    # commits
    (r'^projects/(.*)/commit/(.*)$', commits.show),
    
    # projects
    (r'^projects/add-user$', projects.add_user),
    (r'^projects/remove-user$', projects.remove_user),
    (r'^projects/add$', projects.add),
    (r'^projects/list$', projects.list),
    (r'^projects/(.*)/upload-screenshot$', projects.upload_screenshot),
    (r'^projects/(.*)/modify/(\d+)$', projects.modify),
    (r'^projects/(.*)/modify$', projects.modify),
    (r'^projects/(.*)/blog$', blogs.show_blog),
    (r'^projects/(.*)$', projects.show),
    (r'^projects$', projects.list),
    
    # feed
    (r'^feed$', feed.feed),
    
    # serve media (for now)
    (r'^site-media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    
    (r'$', feed.feed),
)
