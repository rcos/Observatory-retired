import pytest
from django.core.urlresolvers import reverse

@pytest.mark.django_db
def test_reverse_feed():
    a = reverse('dashboard.views.feed.feed')

@pytest.mark.django_db
def test_homepage(client):

    #Load HomePage
    response = client.get('/')

    #Check for normal processing
    assert response.status_code == 200
