import pytest
from dashboard.models import Project, Blog, Repository
from emaillist.models import EmailAddress
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_fetch_warning():

    user = User.objects.create_user('a', 'vagrant@test.rcos.rpi.edu', 'bob')
    user.first_name = "testf"
    user.last_name = "testf"
    user.save()
    email = EmailAddress(address='vagrant@test.rcos.rpi.edu', user=user)
    email.save()

    ease_blog = Blog(from_feed = False)
    ease_blog.save()
    ease_repo = Repository(web_url = "http://git.gnome.org/browse/ease",
        clone_url = "git://git.gnome.org/ease",
        from_feed = False)
    ease_repo.save()
    ease = Project(title = "Ease",
        description = "A presentation application for the Gnome Desktop.",
        website = "http://www.ease-project.org",
        wiki = "http://live.gnome.org/Ease",
        blog_id = ease_blog.id,
        repository_id = ease_repo.id)
    ease.save()
    ease.authors.add(user)
    ease.save()

    ease.do_warnings()
    assert ease.blog_warn_level > 0
    assert ease.repo_warn_level > 0
