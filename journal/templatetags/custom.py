from django import template

register = template.Library()


def string_trans(value):
    return value.replace(" ", "_")


register.filter('string_trans', string_trans)
