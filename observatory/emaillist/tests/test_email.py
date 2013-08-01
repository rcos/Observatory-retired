import pytest
from emaillist.models import EmailExclusion

@pytest.mark.django_db
def test_email_exclude(client):

        #Load Site
        response = client.get('/email/remove/colin@daedrum.net')

        #Check for normal processing
        assert response.status_code in [200, 301]

        assert EmailExclusion.objects.filter(email="colin@daedrum.net").exists()
