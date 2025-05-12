from .models import *

def categorias(request):
    categorias = Producto.CATEGORIAS
    return {'categorias': categorias}

def colores(request):
    colores = Producto.COLORES
    return {'colores': colores}



def notificaciones_usuario(request):
    if request.session.get("pista"):
        usuario_id = request.session["pista"]["id"]
        usuario = Usuario.objects.get(pk=usuario_id)
        notificaciones = Notificacion.objects.filter(usuario=usuario).order_by('-fecha')[:10]
        return {"notificaciones_usuario": notificaciones}
    return {"notificaciones_usuario": []}