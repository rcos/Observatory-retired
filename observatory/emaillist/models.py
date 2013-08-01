from django.db import models

class EmailExclusion(models.Model):
    email = models.CharField(max_length=200)

    @staticmethod
    def excluded(email):
        return EmailExclusion.objects.filter(email=email).exists()
