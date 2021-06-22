from django import template

register = template.Library()

@register.filter
def ampersand(value):
    return value.replace("&", "%26")
