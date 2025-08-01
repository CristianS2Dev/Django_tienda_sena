from .models import *

def categorias(request):
    # Devolver las categorías estáticas desde el modelo Producto
    return {'categorias': Producto.CATEGORIAS}

def colores(request):
    colores = Producto.COLORES
    return {'colores': colores}



def notificaciones_usuario(request):
    """
    Context processor para notificaciones de usuario.
    """
    if request.session.get("pista"):
        usuario_id = request.session["pista"]["id"]
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            # Obtener el queryset base de notificaciones
            notificaciones_queryset = Notificacion.objects.filter(usuario=usuario).order_by('-fecha')
            
            # Contar notificaciones no leídas ANTES del slice
            no_leidas = notificaciones_queryset.filter(leida=False).count()
            
            # Obtener las últimas 20 notificaciones para mostrar
            notificaciones = notificaciones_queryset[:20]
            
            return {
                "notificaciones_usuario": notificaciones,
                "notificaciones_no_leidas": no_leidas
            }
        except Usuario.DoesNotExist:
            pass
    return {
        "notificaciones_usuario": [],
        "notificaciones_no_leidas": 0
    }