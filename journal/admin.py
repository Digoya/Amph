from django.contrib import admin
from .models import UserProfile, Article, Tag

admin.site.register(UserProfile)
admin.site.register(Article)
admin.site.register(Tag)
