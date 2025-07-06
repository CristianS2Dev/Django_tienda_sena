"""
Utilidades para el procesamiento de imágenes
"""
import os
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
import uuid


def optimizar_imagen(imagen, formato='WebP', calidad=85, max_ancho=800, max_alto=800):
    """
    Optimiza una imagen convirtiéndola al formato especificado y redimensionándola.
    
    Args:
        imagen: Archivo de imagen subido
        formato: Formato de salida ('WebP', 'JPEG', 'PNG')
        calidad: Calidad de compresión (1-100)
        max_ancho: Ancho máximo en píxeles
        max_alto: Alto máximo en píxeles
    
    Returns:
        InMemoryUploadedFile: Imagen optimizada
    """
    try:
        # Abrir la imagen
        img = Image.open(imagen)
        
        # Corregir orientación automáticamente basada en EXIF
        img = ImageOps.exif_transpose(img)
        
        # Convertir a RGB si es necesario (para WebP y JPEG)
        if formato in ['WebP', 'JPEG'] and img.mode in ['RGBA', 'P']:
            # Crear un fondo blanco para imágenes con transparencia
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Redimensionar manteniendo proporción
        img.thumbnail((max_ancho, max_alto), Image.Resampling.LANCZOS)
        
        # Crear buffer para la imagen optimizada
        output = BytesIO()
        
        # Configurar parámetros según el formato
        save_params = {'format': formato}
        
        if formato == 'WebP':
            save_params.update({
                'quality': calidad,
                'method': 6,  # Mejor compresión
                'optimize': True
            })
            extension = 'webp'
        elif formato == 'JPEG':
            save_params.update({
                'quality': calidad,
                'optimize': True,
                'progressive': True
            })
            extension = 'jpg'
        elif formato == 'PNG':
            save_params.update({
                'optimize': True
            })
            extension = 'png'
        
        # Guardar la imagen optimizada
        img.save(output, **save_params)
        output.seek(0)
        
        # Generar nombre único
        nombre_original = os.path.splitext(imagen.name)[0]
        nombre_nuevo = f"{nombre_original}_{uuid.uuid4().hex[:8]}.{extension}"
        
        # Crear archivo optimizado
        imagen_optimizada = InMemoryUploadedFile(
            output,
            'ImageField',
            nombre_nuevo,
            f'image/{extension}',
            output.getbuffer().nbytes,
            None
        )
        
        return imagen_optimizada
        
    except Exception as e:
        raise ValidationError(f"Error al procesar la imagen: {str(e)}")


def crear_miniatura(imagen, tamaño=(300, 300)):
    """
    Crea una miniatura de la imagen.
    
    Args:
        imagen: Archivo de imagen
        tamaño: Tupla (ancho, alto) para la miniatura
    
    Returns:
        InMemoryUploadedFile: Miniatura
    """
    return optimizar_imagen(
        imagen, 
        formato='WebP', 
        calidad=80, 
        max_ancho=tamaño[0], 
        max_alto=tamaño[1]
    )


def validar_imagen_mejorada(imagen, max_size_mb=5, formatos_permitidos=None):
    """
    Validación mejorada para imágenes.
    
    Args:
        imagen: Archivo de imagen subido
        max_size_mb: Tamaño máximo en MB
        formatos_permitidos: Lista de tipos MIME permitidos
    
    Raises:
        ValidationError: Si la imagen no es válida
    """
    if formatos_permitidos is None:
        formatos_permitidos = [
            'image/jpeg', 'image/jpg', 'image/png', 
            'image/webp', 'image/gif'
        ]
    
    # Validar tipo de archivo
    if imagen.content_type not in formatos_permitidos:
        raise ValidationError(
            f"Formato no permitido: {imagen.content_type}. "
            f"Formatos aceptados: {', '.join(formatos_permitidos)}"
        )
    
    # Validar tamaño
    if imagen.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f"El archivo excede el tamaño máximo de {max_size_mb} MB. "
            f"Tamaño actual: {imagen.size / (1024*1024):.2f} MB"
        )
    
    # Validar que sea una imagen válida
    try:
        img = Image.open(imagen)
        img.verify()
        imagen.seek(0)  # Resetear el puntero del archivo
    except Exception:
        raise ValidationError("El archivo no es una imagen válida.")
    
    # Validar dimensiones mínimas
    imagen.seek(0)
    img = Image.open(imagen)
    ancho, alto = img.size
    
    if ancho < 100 or alto < 100:
        raise ValidationError(
            f"La imagen debe tener al menos 100x100 píxeles. "
            f"Dimensiones actuales: {ancho}x{alto}"
        )
    
    imagen.seek(0)


def obtener_info_imagen(imagen):
    """
    Obtiene información detallada de una imagen.
    
    Args:
        imagen: Archivo de imagen
    
    Returns:
        dict: Información de la imagen
    """
    try:
        img = Image.open(imagen)
        info = {
            'formato': img.format,
            'modo': img.mode,
            'tamaño': img.size,
            'ancho': img.size[0],
            'alto': img.size[1],
            'tamaño_archivo': imagen.size,
            'tamaño_archivo_mb': round(imagen.size / (1024*1024), 2)
        }
        imagen.seek(0)
        return info
    except Exception as e:
        return {'error': str(e)}
