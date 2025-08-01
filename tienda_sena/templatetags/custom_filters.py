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

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento."""
    try:
        # Convertir ambos valores a números decimales para mayor precisión
        from decimal import Decimal, InvalidOperation
        
        if hasattr(value, '__float__') or isinstance(value, (int, float)):
            val = Decimal(str(value))
        else:
            val = Decimal(str(value))
            
        if hasattr(arg, '__float__') or isinstance(arg, (int, float)):
            argument = Decimal(str(arg))
        else:
            argument = Decimal(str(arg))
            
        result = val * argument
        return float(result)
    except (ValueError, TypeError, InvalidOperation):
        return 0

@register.filter
def sub(value, arg):
    """Resta el argumento del valor."""
    try:
        # Convertir ambos valores a números decimales para mayor precisión
        from decimal import Decimal, InvalidOperation
        
        if hasattr(value, '__float__') or isinstance(value, (int, float)):
            val = Decimal(str(value))
        else:
            val = Decimal(str(value))
            
        if hasattr(arg, '__float__') or isinstance(arg, (int, float)):
            argument = Decimal(str(arg))
        else:
            argument = Decimal(str(arg))
            
        result = val - argument
        return float(result)
    except (ValueError, TypeError, InvalidOperation):
        return 0

@register.filter
def div(value, arg):
    """Divide el valor por el argumento."""
    try:
        # Convertir ambos valores a números decimales para mayor precisión
        from decimal import Decimal, InvalidOperation
        
        if hasattr(value, '__float__') or isinstance(value, (int, float)):
            val = Decimal(str(value))
        else:
            val = Decimal(str(value))
            
        if hasattr(arg, '__float__') or isinstance(arg, (int, float)):
            argument = Decimal(str(arg))
        else:
            argument = Decimal(str(arg))
            
        # Evitar división por cero
        if argument == 0:
            return 0
            
        result = val / argument
        return float(result)
    except (ValueError, TypeError, InvalidOperation):
        return 0

@register.filter
def has_user_id(session_pista):
    """Verifica si la sesión tiene un ID de usuario válido."""
    if session_pista and hasattr(session_pista, 'get'):
        user_id = session_pista.get('id')
        return user_id is not None and str(user_id).strip() != ''
    elif session_pista and isinstance(session_pista, dict):
        user_id = session_pista.get('id')
        return user_id is not None and str(user_id).strip() != ''
    return False

@register.filter
def safe_file_url(field):
    """Obtiene la URL de un archivo de forma segura, retorna cadena vacía si no existe."""
    try:
        if field and hasattr(field, 'url') and field.name:
            return field.url
    except (ValueError, AttributeError):
        pass
    return ''

@register.filter
def safe_file_size(field):
    """Obtiene el tamaño de un archivo de forma segura, retorna 0 si no existe."""
    try:
        if field and hasattr(field, 'size') and field.name:
            return field.size
    except (ValueError, AttributeError):
        pass
    return 0

@register.filter
def has_file(field):
    """Verifica si un campo de archivo tiene un archivo asociado."""
    try:
        return field and hasattr(field, 'name') and field.name and bool(field.name.strip())
    except (ValueError, AttributeError):
        return False

@register.filter
def get_item(dictionary, key):
    """Obtiene un item de un diccionario usando la clave."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def decimal_or_empty(value):
    """Convierte un valor decimal a string o devuelve cadena vacía si es None."""
    if value is None:
        return ""
    return str(value)

@register.filter
def decimal_or_zero(value):
    """Convierte un valor decimal a string o devuelve '0' si es None."""
    if value is None:
        return "0"
    return str(value)

@register.filter
def star_range(rating):
    """
    Genera un rango de estrellas basado en la calificación.
    Retorna una lista de diccionarios con tipo de estrella para cada posición.
    """
    if rating is None:
        rating = 0
    
    rating = float(rating)
    stars = []
    
    for i in range(1, 6):  # 5 estrellas
        if rating >= i:
            stars.append({'type': 'full'})  # Estrella llena
        elif rating >= i - 0.5:
            stars.append({'type': 'half'})  # Media estrella
        else:
            stars.append({'type': 'empty'})  # Estrella vacía
    
    return stars