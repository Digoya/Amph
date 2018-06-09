from django import template
from journal.models import UserProfile
register = template.Library()


def string_trans(value):
    return value.replace(" ", "_")

register.filter('string_trans', string_trans)
