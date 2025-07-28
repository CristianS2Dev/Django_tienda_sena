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

@register.filter
def cloudinary_responsive(imagen_producto, size="medium"):
    """
    Filtro para URLs responsive automáticas.
    
    Uso en template:
    {{ imagen|cloudinary_responsive:"small" }}
    
    Tamaños disponibles: thumbnail, small, medium, large, original
    """
    if not imagen_producto or not imagen_producto.usa_cloudinary:
        return imagen_segura_url(imagen_producto.imagen if imagen_producto else None)
    
    size_configs = {
        'thumbnail': {'width': 150, 'height': 150, 'crop': 'fill'},
        'small': {'width': 300, 'height': 300, 'crop': 'limit'},
        'medium': {'width': 600, 'height': 600, 'crop': 'limit'},
        'large': {'width': 1200, 'height': 1200, 'crop': 'limit'},
        'original': {'quality': 'auto', 'fetch_format': 'auto'}
    }
    
    config = size_configs.get(size, size_configs['medium'])
    
    return cloudinary_url(imagen_producto.cloudinary_public_id, **config)

@register.filter  
def cloudinary_webp(imagen_producto, width=None):
    """
    Filtro para generar versión WebP optimizada.
    
    Uso en template:
    {{ imagen|cloudinary_webp:400 }}
    """
    if not imagen_producto or not imagen_producto.usa_cloudinary:
        try:
            return imagen_producto.imagen.url if imagen_producto and imagen_producto.imagen else ""
        except:
            return ""
    
    params = {
        'fetch_format': 'webp',
        'quality': 'auto:good',
        'flags': 'progressive'
    }
    
    if width:
        params['width'] = width
        params['crop'] = 'scale'
    
    return cloudinary_url(imagen_producto.cloudinary_public_id, **params)

@register.simple_tag
def cloudinary_picture(imagen_producto, alt_text="", css_class="", img_id="", data_zoom=""):
    """
    Tag para generar elemento <picture> con múltiples formatos.
    
    Uso en template:
    {% cloudinary_picture imagen "Alt text" "css-class" "img-id" "zoom-url" %}
    """
    if not imagen_producto:
        return mark_safe(f'<div class="placeholder-image {css_class}"><i class="bi bi-image"></i></div>')
    
    if not imagen_producto.usa_cloudinary:
        try:
            url = imagen_producto.imagen.url if imagen_producto.imagen else ""
            if url:
                img_attrs = f'src="{url}" alt="{alt_text}" class="{css_class}"'
                if img_id:
                    img_attrs += f' id="{img_id}"'
                if data_zoom:
                    img_attrs += f' data-zoom="{data_zoom}"'
                else:
                    img_attrs += f' data-zoom="{url}"'
                img_attrs += ' loading="lazy"'
                return mark_safe(f'<img {img_attrs}>')
            return ""
        except:
            return mark_safe(f'<div class="placeholder-image {css_class}"><i class="bi bi-image"></i></div>')
    
    # URLs para diferentes formatos
    webp_url = cloudinary_url(imagen_producto.cloudinary_public_id, 
                              fetch_format='webp', quality='auto:good')
    jpg_url = cloudinary_url(imagen_producto.cloudinary_public_id, 
                             fetch_format='jpg', quality='auto')
    
    # URL de zoom en alta calidad
    zoom_url = data_zoom if data_zoom else cloudinary_url(imagen_producto.cloudinary_public_id, 
                                                         width=1500, height=1500, 
                                                         crop="limit", quality="auto", 
                                                         fetch_format="auto")
    
    # Atributos de la imagen - LAS CLASES VAN EN EL IMG, NO EN EL PICTURE
    img_attrs = f'src="{jpg_url}" alt="{alt_text}" class="{css_class}" loading="lazy"'
    if img_id:
        img_attrs += f' id="{img_id}"'
    if zoom_url:
        img_attrs += f' data-zoom="{zoom_url}"'
    
    # Picture sin clases, img con todas las clases para mantener el centrado
    html = f'''<picture>
        <source srcset="{webp_url}" type="image/webp">
        <img {img_attrs}>
    </picture>'''
    
    return mark_safe(html)

@register.filter
def cloudinary_srcset(imagen_producto):
    """
    Filtro para generar srcset responsive.
    
    Uso en template:
    <img srcset="{{ imagen|cloudinary_srcset }}" src="{{ imagen|cloudinary_responsive:'medium' }}">
    """
    if not imagen_producto or not imagen_producto.usa_cloudinary:
        return ""
    
    widths = [300, 600, 900, 1200]
    srcset_parts = []
    
    for width in widths:
        url = cloudinary_url(imagen_producto.cloudinary_public_id, 
                           width=width, 
                           crop='scale', 
                           quality='auto',
                           fetch_format='auto')
        srcset_parts.append(f"{url} {width}w")
    
    return ", ".join(srcset_parts)
