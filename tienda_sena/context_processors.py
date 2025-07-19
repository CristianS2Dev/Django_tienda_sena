from .models import *

def categorias(request):
    # Devolver las categorías estáticas desde el modelo Producto
    return {'categorias': Producto.CATEGORIAS}

def colores(request):
    colores = Producto.COLORES
    return {'colores': colores}



def notificaciones_usuario(request):
    """
    Context processor mejorado para notificaciones.
    Funciona para todos los roles de usuario.
    """
    if request.session.get("pista"):
        usuario_id = request.session["pista"]["id"]
        usuario_rol = request.session["pista"]["rol"]
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            # Obtener el queryset base de notificaciones
            notificaciones_queryset = Notificacion.objects.filter(usuario=usuario).order_by('-fecha')
            
            # Contar notificaciones no leídas ANTES del slice
            no_leidas = notificaciones_queryset.filter(leida=False).count()
            
            # Obtener las últimas 20 notificaciones para mostrar
            notificaciones = notificaciones_queryset[:20]
            
            context = {
                "notificaciones_usuario": notificaciones,
                "notificaciones_no_leidas": no_leidas,
                "notificaciones_admin_pendientes": 0
            }
            
            # Si es administrador, contar notificaciones admin pendientes
            if usuario_rol == 1:  # Es administrador
                admin_notifications = Notificacion.objects.filter(
                    tipo__in=['vendor_request', 'new_user', 'new_product', 'new_order'],
                    fecha_leida=None
                ).count()
                context['notificaciones_admin_pendientes'] = admin_notifications
            
            return context
        except Usuario.DoesNotExist:
            pass
    return {
        "notificaciones_usuario": [],
        "notificaciones_no_leidas": 0,
        "notificaciones_admin_pendientes": 0
    }