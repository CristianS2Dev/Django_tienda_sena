from django import template

register = template.Library()

@register.filter
def replace_comma(value):
    """Reemplaza las comas por puntos en un número."""
    if isinstance(value, str):
        return value.replace(',', '.')
    return value

