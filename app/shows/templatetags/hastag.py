from django import template

register = template.Library()

@register.filter
def hastag(value):
    return value.replace("#", "%23")
