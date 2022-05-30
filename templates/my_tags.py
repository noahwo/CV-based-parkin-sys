
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def multi(v1, v2, v3):
    return v1 * v2 * v3


@register.simple_tag
def sum(v1, v2, v3):
    return v1 + v2 + v3
