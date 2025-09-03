from django import template

register = template.Library()

@register.filter
def format_name(value):
    """Replace underscores with spaces and capitalize words."""
    if value:
        return value.replace('_', ' ').title()
    return ""
