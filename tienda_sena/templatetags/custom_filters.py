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
    Ej: {% for grupo en marcas|group_by:4 %}
    """
    arg = int(arg)
    return [value[i:i + arg] for i in range(0, len(value), arg)]

@register.filter
def total_vendedor(items_vendidos, orden_id):
    """ Calcula el total vendido por un vendedor en una orden específica. """
    return sum(item.cantidad * item.precio_unitario for item in items_vendidos if item.orden.id == orden_id)