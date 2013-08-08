import pytest
from django.core.urlresolvers import reverse

@pytest.mark.django_db
def test_homepage(client, settings):

    settings.DEBUG = False

    for url in (
            "/",
            "/donor",
            "/students",
            "/courses",
            "/talks",
            "/programming-competition",
            "/achievements",
            "/urp-application",
            "/links-and-contacts",
            "/talk-sign-up",
            "/irc",
            "/faq",
            "/calendar",
            "/howtojoin",
            "/past-projects",
            ):

        #Load Site
        response = client.get(url)

        #Check for normal processing
        assert response.status_code in [200, 301]
