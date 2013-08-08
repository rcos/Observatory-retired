import pytest

@pytest.mark.django_db
def test_dashboard_pages(client, settings):
    settings.DEBUG = False

    for url in (
            "/posts",
            "/register-or-login",
            "/login",
            "/logout",
            "/people",
            "/past_people",
            "/forgot-password",
            "/forgot_password_success/",
            "/commits",
            "/projects/list",
            "/projects/pending",
            "/projects/archive_list",
            "/projects",
            "/feed",
            "/feed.rss"
            ):

        #Load Site
        response = client.get(url)

        #Check for normal processing
        assert response.status_code in [200, 301]
