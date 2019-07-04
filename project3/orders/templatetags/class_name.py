from django import template

register = template.Library()

@register.filter
def class_name(object):
    return object.__class__.__name__
