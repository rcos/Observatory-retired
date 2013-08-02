from django.db import models
from django.contrib.auth.models import User

class EmailAddress(models.Model):

    address = models.CharField(max_length=200, primary_key=True, unique=True)

    #Whether the user clicked the spam button and we should never contact them again
    excluded = models.BooleanField(default=False)

    user = models.ForeignKey(User, related_name="emails", null=True)

    @staticmethod
    def excluded(email):
        try:
            return EmailAddress.object.get(address=email).excluded
        except Emailaddress.DoesNotExist:
            return False
