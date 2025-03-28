from .models import *

def categorias(request):
    categorias = Producto.CATEGORIAS
    return {'categorias': categorias}

def colores(request):
    colores = Producto.COLORES
    return {'colores': colores}