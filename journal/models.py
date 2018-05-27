from django.db import models
"""
    Creating Object user for DB
"""


class User(models.Model):

    username = models.CharField(max_length=40, unique=True, help_text="Enter your login", null=False)

    """
        Representing an object as his login
    """
    def __str__(self):
        return self.username

    password = models.CharField(max_length=40, help_text="Enter your password", null=False)

    email = models.EmailField(help_text="Enter your Email", null=True, blank=True)

    short_describe = models.CharField(max_length=240, help_text="Enter short Description", null=True, blank=True)


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120, null=False)
    short_desc = models.CharField(max_length=240, null=True, blank=True)
    main_text = models.TextField(null=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

