# GuessItGame/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a dynamic key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None


@register.filter
def get_attr(obj, attr_name):
    """Get an attribute from an object using a dynamic attribute name"""
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None
