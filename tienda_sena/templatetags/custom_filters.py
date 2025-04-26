from django import template

register = template.Library()

@register.filter
def replace_comma(value):
    """Reemplaza las comas por puntos en un número."""
    if isinstance(value, str):
        return value.replace(',', '.')
    return value

@register.filter
def group_by(value, arg):
    """
    Agrupa una lista en sublistas de tamaño 'arg'.
    Ej: {% for grupo in marcas|group_by:4 %}
    """
    arg = int(arg)
    return [value[i:i + arg] for i in range(0, len(value), arg)]


@register.filter
def group_by(value, n):
    """ Agrupa una lista en sublistas de n elementos """
    return [value[i:i+n] for i in range(0, len(value), n)]