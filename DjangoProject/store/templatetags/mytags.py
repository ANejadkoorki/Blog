from django import template

register = template.Library()


@register.filter
def jdate(value, format='%Y-%m-%d'):
    """
        formats date on based on 'format
    """
    return value.strftime(format)