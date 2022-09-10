from atexit import register
from django import template

register = template.Library()

# gel_val is a decorater
@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)