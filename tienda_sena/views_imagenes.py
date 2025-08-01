"""
Vistas adicionales para gestión avanzada de imágenes
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ImagenProducto, Producto
from .utils import session_rol_permission
import json


@session_rol_permission(1, 3)
def gestionar_imagenes_producto(request, id_producto):
    """Vista para gestionar las imágenes de un producto específico."""
    producto = get_object_or_404(Producto, id=id_producto)
    
    # Verificar permisos (administrador o dueño del producto)
    usuario_rol = request.session.get("pista")["rol"]
    usuario_id = request.session.get("pista")["id"]
    
    if usuario_rol != 1 and producto.vendedor_id != usuario_id:
        messages.error(request, "No tienes permisos para gestionar las imágenes de este producto.")
        return redirect("lista_productos")
    
    # Manejar subida de nuevas imágenes
    if request.method == "POST":
        imagenes_nuevas = request.FILES.getlist("imagenes_nuevas")
        
        if imagenes_nuevas:
            try:
                # Validar cantidad de imágenes
                if len(imagenes_nuevas) > 5:
                    messages.error(request, "Solo puedes subir hasta 5 imágenes a la vez.")
                    return redirect("gestionar_imagenes_producto", id_producto=id_producto)
                
                # Validar formato y tamaño
                formatos_permitidos = ['jpg', 'jpeg', 'png', 'webp']
                for imagen in imagenes_nuevas:
                    if not imagen.name.lower().split('.')[-1] in formatos_permitidos:
                        messages.error(request, f"Formato de imagen no permitido: {imagen.name}")
                        return redirect("gestionar_imagenes_producto", id_producto=id_producto)
                    if imagen.size < 10000:
                        messages.error(request, f"La imagen {imagen.name} es demasiado pequeña (mínimo 10KB).")
                        return redirect("gestionar_imagenes_producto", id_producto=id_producto)
                
                # Importar función de procesamiento
                from .views import procesar_imagen_producto
                from django.db import models
                
                # Procesar imágenes
                imagenes_procesadas = []
                for i, imagen in enumerate(imagenes_nuevas):
                    resultado = procesar_imagen_producto(imagen)
                    if not resultado['success']:
                        messages.error(request, f"Error en imagen {i+1}: {resultado['error']}")
                        return redirect("gestionar_imagenes_producto", id_producto=id_producto)
                    imagenes_procesadas.append(resultado)
                
                # Obtener el próximo número de orden
                ultimo_orden = ImagenProducto.objects.filter(producto=producto).aggregate(
                    max_orden=models.Max('orden'))['max_orden'] or 0
                
                # Guardar las nuevas imágenes
                for i, resultado in enumerate(imagenes_procesadas):
                    imagen_producto = ImagenProducto(
                        producto=producto,
                        imagen_original=imagenes_nuevas[i],
                        imagen=resultado['imagen_optimizada'],
                        miniatura=resultado['miniatura'],
                        es_principal=False,
                        orden=ultimo_orden + i + 1
                    )
                    imagen_producto.save()
                
                messages.success(request, f"Se agregaron {len(imagenes_procesadas)} imágenes exitosamente.")
                return redirect("gestionar_imagenes_producto", id_producto=id_producto)
                
            except Exception as e:
                messages.error(request, f"Error procesando imágenes: {str(e)}")
                return redirect("gestionar_imagenes_producto", id_producto=id_producto)
    
    imagenes = producto.imagenes.all().order_by('orden', 'id')
    
    context = {
        'producto': producto,
        'imagenes': imagenes,
    }
    
    return render(request, 'productos/gestionar_imagenes.html', context)


@require_POST
@session_rol_permission(1, 3)
def establecer_imagen_principal(request, id_imagen):
    """Establece una imagen como principal del producto."""
    imagen = get_object_or_404(ImagenProducto, id=id_imagen)
    
    # Verificar permisos
    usuario_rol = request.session.get("pista")["rol"]
    usuario_id = request.session.get("pista")["id"]
    
    if usuario_rol != 1 and imagen.producto.vendedor_id != usuario_id:
        return JsonResponse({'success': False, 'error': 'Sin permisos'})
    
    # Desmarcar imagen principal actual
    ImagenProducto.objects.filter(
        producto=imagen.producto, 
        es_principal=True
    ).update(es_principal=False)
    
    # Marcar nueva imagen como principal
    imagen.es_principal = True
    imagen.save()
    
    return JsonResponse({'success': True})


@require_POST
@session_rol_permission(1, 3)
def eliminar_imagen_producto(request, id_imagen):
    """Elimina una imagen de producto."""
    imagen = get_object_or_404(ImagenProducto, id=id_imagen)
    
    # Verificar permisos
    usuario_rol = request.session.get("pista")["rol"]
    usuario_id = request.session.get("pista")["id"]
    
    if usuario_rol != 1 and imagen.producto.vendedor_id != usuario_id:
        return JsonResponse({'success': False, 'error': 'Sin permisos'})
    
    # No permitir eliminar si es la única imagen
    if imagen.producto.imagenes.count() <= 1:
        return JsonResponse({
            'success': False, 
            'error': 'No puedes eliminar la única imagen del producto'
        })
    
    producto_id = imagen.producto.id
    era_principal = imagen.es_principal
    
    # Eliminar imagen
    imagen.delete()
    
    # Si era principal, establecer otra como principal
    if era_principal:
        primera_imagen = ImagenProducto.objects.filter(
            producto_id=producto_id
        ).order_by('orden', 'id').first()
        
        if primera_imagen:
            primera_imagen.es_principal = True
            primera_imagen.save()
    
    return JsonResponse({'success': True})


@require_POST
@csrf_exempt
@session_rol_permission(1, 3)
def reordenar_imagenes(request):
    """Reordena las imágenes de un producto."""
    try:
        data = json.loads(request.body)
        orden_imagenes = data.get('orden', [])
        
        if not orden_imagenes:
            return JsonResponse({'success': False, 'error': 'Orden vacío'})
        
        # Verificar que todas las imágenes pertenezcan al mismo producto
        imagenes = ImagenProducto.objects.filter(id__in=orden_imagenes)
        productos = set(img.producto_id for img in imagenes)
        
        if len(productos) != 1:
            return JsonResponse({'success': False, 'error': 'Imágenes de diferentes productos'})
        
        producto_id = list(productos)[0]
        
        # Verificar permisos
        usuario_rol = request.session.get("pista")["rol"]
        usuario_id = request.session.get("pista")["id"]
        producto = Producto.objects.get(id=producto_id)
        
        if usuario_rol != 1 and producto.vendedor_id != usuario_id:
            return JsonResponse({'success': False, 'error': 'Sin permisos'})
        
        # Actualizar orden
        for i, imagen_id in enumerate(orden_imagenes):
            ImagenProducto.objects.filter(id=imagen_id).update(orden=i)
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def estadisticas_imagenes(request):
    """Vista para mostrar estadísticas de optimización de imágenes."""
    if not request.session.get("pista") or request.session.get("pista")["rol"] != 1:
        messages.error(request, "Acceso denegado.")
        return redirect("index")
    
    from django.db.models import Count, Sum
    import os
    
    # Estadísticas básicas
    stats = {
        'total_productos': Producto.objects.count(),
        'productos_con_imagenes': Producto.objects.filter(imagenes__isnull=False).distinct().count(),
        'total_imagenes': ImagenProducto.objects.count(),
        'imagenes_principales': ImagenProducto.objects.filter(es_principal=True).count(),
    }
    
    # Calcular tamaños aproximados (esto puede ser lento en producción)
    try:
        tamaño_total = 0
        tamaño_originales = 0
        contador = 0
        
        for imagen in ImagenProducto.objects.all()[:100]:  # Limitar para demo
            if imagen.imagen and os.path.exists(imagen.imagen.path):
                tamaño_total += os.path.getsize(imagen.imagen.path)
                contador += 1
            
            if imagen.imagen_original and os.path.exists(imagen.imagen_original.path):
                tamaño_originales += os.path.getsize(imagen.imagen_original.path)
        
        if contador > 0:
            stats['tamaño_optimizado_mb'] = round(tamaño_total / (1024*1024), 2)
            stats['tamaño_original_mb'] = round(tamaño_originales / (1024*1024), 2)
            stats['ahorro_porcentaje'] = round(
                ((tamaño_originales - tamaño_total) / tamaño_originales * 100) 
                if tamaño_originales > 0 else 0, 2
            )
        
    except Exception as e:
        stats['error_calculo'] = str(e)
    
    return render(request, 'administrador/estadisticas_imagenes.html', {'stats': stats})
