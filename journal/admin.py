from django.contrib import admin
from journal import models

admin.site.register(models.UserProfile)
admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.EmailVerification)
admin.site.register(models.Journal)
