from django.db import models
from django.contrib.auth.models import User
"""
    Creating Object user for DB
"""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    short_describe = models.CharField(max_length=240, help_text="Enter short Description", null=True, blank=True)
    subscribers = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120, null=False)
    short_desc = models.CharField(max_length=240, null=True, blank=True)
    main_text = models.TextField(null=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

