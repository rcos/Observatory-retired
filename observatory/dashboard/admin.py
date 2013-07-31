from models import *
from django.contrib import admin
from django.contrib.auth.models import User, Group

for model in (
                AuthorRequest,
                Blog,
                BlogPost,
                Commit,
                Contributor,
                Event,
                Repository,
                Screenshot,
                UserInfo,
                ):
    admin.site.register(model)

for model, modeladmin in [
    (Project, ProjectAdmin),
    ]:
    admin.site.register(model, modeladmin)

