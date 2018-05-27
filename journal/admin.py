from django.contrib import admin
from .models import User, Article, Tag

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Tag)

