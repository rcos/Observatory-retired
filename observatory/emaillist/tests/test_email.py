import pytest
from emaillist.models import EmailAddress

@pytest.mark.django_db
def test_email_exclude(client):

        m = EmailAddress(address="colin@daedrum.net")
        m.save()

        #Load Site
        response = client.get('/email/remove/colin@daedrum.net')

        #Check for normal processing
        assert response.status_code in [200, 301]

        assert EmailAddress.objects.filter(address="colin@daedrum.net").get().excluded
