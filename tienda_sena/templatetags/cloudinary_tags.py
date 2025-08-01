"""
Template tags personalizados para Cloudinary en Tienda SENA
"""
from django import template
from django.utils.safestring import mark_safe
from cloudinary import CloudinaryImage
import cloudinary.utils

register = template.Library()

@register.simple_tag
def cloudinary_url(public_id, **kwargs):
    """
    Genera URL de Cloudinary con transformaciones opcionales.
    
    Uso en template:
    {% cloudinary_url imagen.cloudinary_public_id width=300 height=300 crop="fill" %}
    """
    if not public_id:
        return ""
    
    try:
        return CloudinaryImage(public_id).build_url(**kwargs)
    except Exception:
        return ""

@register.simple_tag
def cloudinary_thumbnail(public_id, width=300, height=300):
    """
    Genera URL de miniatura optimizada.
    
    Uso en template:
    {% cloudinary_thumbnail imagen.cloudinary_public_id 300 300 %}
    """
    if not public_id:
        return ""
    
    return cloudinary_url(public_id, 
                         width=width, 
                         height=height, 
                         crop="fill", 
                         quality="auto", 
                         fetch_format="auto")

@register.simple_tag
def cloudinary_responsive(public_id, **kwargs):
    """
    Genera URL responsiva que se adapta al dispositivo.
    
    Uso en template:
    {% cloudinary_responsive imagen.cloudinary_public_id width="auto" crop="scale" %}
    """
    if not public_id:
        return ""
    
    # Configuración por defecto para responsive
    default_kwargs = {
        'width': 'auto',
        'crop': 'scale',
        'quality': 'auto',
        'fetch_format': 'auto',
        'dpr': 'auto'
    }
    default_kwargs.update(kwargs)
    
    return cloudinary_url(public_id, **default_kwargs)

@register.inclusion_tag('cloudinary/image_tag.html')
def cloudinary_image(imagen_producto, alt_text="", css_class="", **kwargs):
    """
    Renderiza una imagen completa con fallback.
    
    Uso en template:
    {% cloudinary_image producto.imagen_principal "Descripción" "img-fluid" width=400 %}
    """
    context = {
        'imagen_producto': imagen_producto,
        'alt_text': alt_text,
        'css_class': css_class,
    }
    
    if imagen_producto:
        if imagen_producto.usa_cloudinary and imagen_producto.cloudinary_public_id:
            # Usar Cloudinary
            context['cloudinary_url'] = cloudinary_url(imagen_producto.cloudinary_public_id, **kwargs)
            context['usa_cloudinary'] = True
        elif imagen_producto.imagen:
            # Fallback a imagen local
            context['local_url'] = imagen_producto.imagen.url
            context['usa_cloudinary'] = False
    
    return context

@register.simple_tag
def cloudinary_product_gallery(producto, **kwargs):
    """
    Genera URLs para galería de producto.
    
    Uso en template:
    {% cloudinary_product_gallery producto width=800 height=600 %}
    """
    urls = []
    
    for imagen in producto.imagenes.all().order_by('orden'):
        if imagen.usa_cloudinary and imagen.cloudinary_public_id:
            url = cloudinary_url(imagen.cloudinary_public_id, **kwargs)
            urls.append({
                'url': url,
                'thumbnail': cloudinary_thumbnail(imagen.cloudinary_public_id),
                'es_principal': imagen.es_principal,
                'orden': imagen.orden
            })
        elif imagen.imagen:
            urls.append({
                'url': imagen.imagen.url,
                'thumbnail': imagen.imagen.url,
                'es_principal': imagen.es_principal,
                'orden': imagen.orden
            })
    
    return urls

@register.filter
def cloudinary_zoom(imagen_producto):
    """
    Filtro para URL de zoom en detalle de producto.
    
    Uso en template:
    {{ producto.imagen_principal|cloudinary_zoom }}
    """
    if not imagen_producto:
        return ""
    
    if imagen_producto.usa_cloudinary and imagen_producto.cloudinary_public_id:
        return cloudinary_url(imagen_producto.cloudinary_public_id, 
                             width=1500, 
                             height=1500, 
                             crop="limit", 
                             quality="auto", 
                             fetch_format="auto")
    elif imagen_producto.imagen:
        return imagen_producto.imagen.url
    
    return ""

@register.filter
def cloudinary_banner(imagen_producto):
    """
    Filtro para URL de banner en listado.
    
    Uso en template:
    {{ producto.imagen_principal|cloudinary_banner }}
    """
    if not imagen_producto:
        return ""
    
    if imagen_producto.usa_cloudinary and imagen_producto.cloudinary_public_id:
        return cloudinary_url(imagen_producto.cloudinary_public_id, 
                             width=1200, 
                             height=400, 
                             crop="fill", 
                             quality="auto", 
                             fetch_format="auto")
    elif imagen_producto.imagen:
        return imagen_producto.imagen.url
    
    return ""

@register.simple_tag
def cloudinary_profile_image(usuario, size=150):
    """
    Genera URL de imagen de perfil optimizada.
    
    Uso en template:
    {% cloudinary_profile_image usuario 200 %}
    """
    # Aquí asumimos que también actualizarás el modelo Usuario para Cloudinary
    # Por ahora retorna la imagen local si existe
    if hasattr(usuario, 'imagen_perfil') and usuario.imagen_perfil:
        return usuario.imagen_perfil.url
    else:
        # Imagen por defecto
        return "/static/img/profile_default.png"

@register.simple_tag
def cloudinary_stats(producto):
    """
    Obtiene estadísticas de optimización de imágenes del producto.
    
    Uso en template:
    {% cloudinary_stats producto as stats %}
    {{ stats.total_imagenes }} imágenes optimizadas
    """
    imagenes = producto.imagenes.all()
    cloudinary_count = imagenes.filter(usa_cloudinary=True).count()
    local_count = imagenes.filter(usa_cloudinary=False).count()
    
    return {
        'total_imagenes': imagenes.count(),
        'cloudinary_imagenes': cloudinary_count,
        'local_imagenes': local_count,
        'porcentaje_cloudinary': (cloudinary_count / imagenes.count() * 100) if imagenes.count() > 0 else 0
    }

@register.simple_tag
def producto_imagen_url(producto, transformacion=None):
    """
    Obtiene URL de imagen principal de producto de manera segura.
    
    Uso en template:
    {% producto_imagen_url producto %}
    {% producto_imagen_url producto "{'width': 400, 'height': 300}" %}
    """
    if not producto:
        from django.templatetags.static import static
        return static('assets/product.png')
    
    return producto.get_imagen_principal_url(transformacion)

@register.simple_tag
def producto_imagen_thumbnail(producto, width=300, height=300):
    """
    Obtiene thumbnail de imagen principal de producto.
    
    Uso en template:
    {% producto_imagen_thumbnail producto 400 300 %}
    """
    transformacion = {
        'width': width,
        'height': height,
        'crop': 'fill',
        'quality': 'auto',
        'fetch_format': 'auto'
    }
    return producto_imagen_url(producto, transformacion)

@register.simple_tag
def imagen_segura_url(imagen_producto, transformacion=None):
    """
    Obtiene URL de imagen de manera segura, manejando errores.
    
    Uso en template:
    {% imagen_segura_url imagen %}
    """
    if not imagen_producto:
        from django.templatetags.static import static
        return static('assets/product.png')
    
    try:
        url = imagen_producto.get_imagen_url(transformacion)
        if url:
            return url
    except Exception:
        pass
    
    # Fallback a imagen por defecto
    from django.templatetags.static import static
    return static('assets/product.png')
