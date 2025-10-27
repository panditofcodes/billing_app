from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Safely get an attribute of an object in templates."""
    return getattr(obj, attr, '')
