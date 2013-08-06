from dashboard.feeds import *
from dashboard.views import *
from django.conf.urls import *

urlpatterns = patterns('',

    # author requests
    (r'^author-request/approve/(\d+)/$', author_requests.approve),
    (r'^author-request/reject/(\d+)/$', author_requests.reject),

    # blog posts
    (r'^posts/add/(\d+)/$', blogs.write_post),
    (r'^posts/create/(\d+)/$', blogs.create_post),
    (r'^posts/page/(\d+)/$', blogs.posts_page),
    (r'^project/([^\.]*)/post/([^\.]*)/modify/$', blogs.edit_post),
    (r'^project/([^\.]*)/post/([^\.]*)/update/$', blogs.update_post),
    (r'^project/([^\.]*)/post/([^\.]*)/delete/$', blogs.delete_post),
    (r'^project/([^\.]*)/post/([^\.]*)/$', blogs.show_post),
    (r'^post/([^\.]*)/$', blogs.show_user_post),
    (r'^project/([^\.]*)/post/([^\.]*)\.rss$',
     SingleFeed(),  {'model': BlogPost}),

    (r'^projects/([^\.]*)/posts/$', blogs.show_blog),
    (r'^projects/([^\.]*)/posts\.rss$', BlogPostsFeed()),

    (r'^posts/$', blogs.posts),
    (r'^posts\.rss$', BlogPostsFeed()),

    # users
    (r'^register-or-login/$', users.login_or_reg),
    (r'^register/$', users.register),
    (r'^login/$', users.login),
    (r'^logout/$', users.logout),
    (r'^user/(\d+)/commits/$', commits.show_user),
    (r'^user/(\d+)/posts/personal/remove/$', blogs.remove_personal_blog),
    (r'^user/(\d+)/posts/personal/$', blogs.edit_personal_blog),
    (r'^user/(\d+)/post/([^\.]*)/$', blogs.show_user_post),
    (r'^user/(\d+)/posts/$', blogs.show_user_blog),
    (r'^user/(\d+)/$', users.profile),
    (r'^people/$', users.people),
    (r'^past_people/$', users.past_people),
    (r'^user_deactivate/(\d+)/$', users.deactivate),
    (r'^user_activate/(\d+)/$', users.activate),
    (r'^forgot-password/$', users.forgot_password),
    (r'^forgot_password_success/$', users.forgot_password_success),

    # commits
    (r'^projects/([^\.]*)/commit/([^\.]*)/$', commits.show),
    (r'^projects/([^\.]*)/commit/([^\.]*)\.rss$',
     SingleFeed(), {'model': Commit}),


    (r'^commits/(\d+)/$', commits.all_page),
    (r'^commits/$', commits.all),
    (r'^commits\.rss$', CommitsFeed()),

    (r'^projects/([^\.]*)/commits/$', commits.show_repository),
    (r'^projects/([^\.]*)/commits/(\d+)/$', commits.repository_page),
    (r'^projects/([^\.]*)/commits\.rss$', CommitsFeed()),

    # projects
    (r'^projects/add-mentor/$', projects.add_mentor),
    (r'^projects/add-user/$', projects.add_user),
    (r'^projects/remove-user/$', projects.remove_user),
    (r'^projects/add/$', projects.add),
    (r'^projects/list/$', projects.list),
	(r'^projects/pending/$', projects.pending_list),
	(r'^projects/pending/approve/([^\.]*)', projects.approve),
	(r'^projects/pending/deny/([^\.]*)', projects.deny),
    (r'^projects/archive_list/$', projects.archived_list),
    (r'^projects/([^\.]*)/delete-screenshot/(\d+)/$',
        projects.delete_screenshot),
    (r'^projects/([^\.]*)/modify/(\d+)/$', projects.modify),
    (r'^projects/([^\.]*)/modify/$', projects.modify),

    (r'^projects/([^\.]*)/$', projects.show),
    (r'^projects/([^\.]*)\.rss', EventsFeed()),

    (r'^projects/$', projects.list),

    # feed
    (r'^event/([^\.]*)/$', feed.event),
    (r'^feed/$', feed.feed),
    (r'^feed\.rss$', EventsFeed()),

)

