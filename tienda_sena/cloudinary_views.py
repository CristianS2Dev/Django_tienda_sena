"""
Funciones mejoradas para el procesamiento de imágenes con Cloudinary
"""
from django.core.exceptions import ValidationError
from .cloudinary_utils import cloudinary_manager
from .models import ImagenProducto
import logging

logger = logging.getLogger(__name__)

def procesar_imagenes_cloudinary(imagenes, producto_id):
    """
    Procesa múltiples imágenes subiéndolas a Cloudinary.
    
    Args:
        imagenes (list): Lista de archivos de imagen
        producto_id (int): ID del producto
    
    Returns:
        dict: Resultado del procesamiento con información detallada
    """
    resultados = []
    errores = []
    total_bytes_original = 0
    total_bytes_optimizado = 0
    
    for i, imagen in enumerate(imagenes):
        try:
            # Validar imagen antes de subir
            cloudinary_manager.validar_imagen(imagen, 'producto')
            
            # Obtener tamaño original
            total_bytes_original += imagen.size
            
            # Subir a Cloudinary
            resultado_cloudinary = cloudinary_manager.subir_imagen_producto(
                imagen, 
                producto_id, 
                es_principal=(i == 0)
            )
            
            if resultado_cloudinary['success']:
                # Calcular tamaño optimizado aproximado (Cloudinary reduce ~60-80%)
                bytes_estimado = imagen.size * 0.3  # Estimación conservadora
                total_bytes_optimizado += bytes_estimado
                
                resultado = {
                    'success': True,
                    'public_id': resultado_cloudinary['public_id'],
                    'version': resultado_cloudinary['version'],
                    'urls': resultado_cloudinary['urls'],
                    'metadata': resultado_cloudinary['metadata'],
                    'orden': i,
                    'es_principal': (i == 0),
                    'bytes_original': imagen.size,
                    'bytes_optimizado': bytes_estimado
                }
                resultados.append(resultado)
                
                logger.info(f"Imagen {i+1} subida exitosamente a Cloudinary: {resultado_cloudinary['public_id']}")
            else:
                errores.append(f"Error en imagen {i+1}: No se pudo subir a Cloudinary")
                
        except ValidationError as e:
            errores.append(f"Error en imagen {i+1}: {str(e)}")
        except Exception as e:
            errores.append(f"Error inesperado en imagen {i+1}: {str(e)}")
            logger.error(f"Error procesando imagen {i+1}: {str(e)}")
    
    # Calcular estadísticas de optimización
    ahorro_porcentaje = 0
    if total_bytes_original > 0:
        ahorro_porcentaje = ((total_bytes_original - total_bytes_optimizado) / total_bytes_original) * 100
    
    return {
        'success': len(errores) == 0,
        'resultados': resultados,
        'errores': errores,
        'estadisticas': {
            'imagenes_procesadas': len(resultados),
            'total_imagenes': len(imagenes),
            'bytes_original': total_bytes_original,
            'bytes_optimizado': total_bytes_optimizado,
            'ahorro_porcentaje': ahorro_porcentaje,
            'mb_original': total_bytes_original / (1024 * 1024),
            'mb_optimizado': total_bytes_optimizado / (1024 * 1024)
        }
    }

def crear_imagenes_producto_cloudinary(resultados_cloudinary, producto):
    """
    Crea objetos ImagenProducto con información de Cloudinary.
    
    Args:
        resultados_cloudinary (list): Lista de resultados de Cloudinary
        producto: Instancia del producto
    
    Returns:
        list: Lista de objetos ImagenProducto creados
    """
    imagenes_creadas = []
    
    for resultado in resultados_cloudinary:
        try:
            imagen_producto = ImagenProducto(
                producto=producto,
                cloudinary_public_id=resultado['public_id'],
                cloudinary_version=str(resultado['version']),
                imagen_cloudinary=resultado['public_id'],  # Configurar campo Cloudinary
                es_principal=resultado['es_principal'],
                orden=resultado['orden'],
                usa_cloudinary=True
            )
            imagen_producto.save()
            imagenes_creadas.append(imagen_producto)
            
            logger.info(f"ImagenProducto creada: {imagen_producto.id} - {resultado['public_id']}")
            
        except Exception as e:
            logger.error(f"Error creando ImagenProducto: {str(e)}")
            # Si falla la creación del objeto, intentar eliminar de Cloudinary
            cloudinary_manager.eliminar_imagen(resultado['public_id'])
    
    return imagenes_creadas

def migrar_imagen_local_a_cloudinary(imagen_producto):
    """
    Migra una imagen local existente a Cloudinary.
    
    Args:
        imagen_producto: Instancia de ImagenProducto con imagen local
    
    Returns:
        bool: True si la migración fue exitosa
    """
    if not imagen_producto.imagen or imagen_producto.cloudinary_public_id:
        return False
    
    try:
        # Abrir la imagen local
        imagen_producto.imagen.open()
        
        # Subir a Cloudinary
        resultado = cloudinary_manager.subir_imagen_producto(
            imagen_producto.imagen,
            imagen_producto.producto.id,
            imagen_producto.es_principal
        )
        
        if resultado['success']:
            # Actualizar el objeto con información de Cloudinary
            imagen_producto.cloudinary_public_id = resultado['public_id']
            imagen_producto.cloudinary_version = str(resultado['version'])
            imagen_producto.usa_cloudinary = True
            
            # Configurar el campo imagen_cloudinary también
            imagen_producto.imagen_cloudinary = resultado['public_id']
            imagen_producto.save()
            
            logger.info(f"Imagen migrada exitosamente: {imagen_producto.id} -> {resultado['public_id']}")
            return True
            
    except Exception as e:
        logger.error(f"Error migrando imagen {imagen_producto.id}: {str(e)}")
    
    return False

def procesar_imagen_perfil_cloudinary(imagen, usuario_id):
    """
    Procesa una imagen de perfil subiéndola a Cloudinary.
    
    Args:
        imagen: Archivo de imagen
        usuario_id: ID del usuario
    
    Returns:
        dict: Resultado del procesamiento
    """
    try:
        # Validar imagen
        cloudinary_manager.validar_imagen(imagen, 'perfil')
        
        # Subir a Cloudinary
        resultado = cloudinary_manager.subir_imagen_perfil(imagen, usuario_id)
        
        if resultado['success']:
            return {
                'success': True,
                'public_id': resultado['public_id'],
                'version': resultado['version'],
                'urls': resultado['urls'],
                'metadata': resultado['metadata']
            }
        else:
            return {
                'success': False,
                'error': 'No se pudo subir la imagen a Cloudinary'
            }
            
    except ValidationError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        logger.error(f"Error procesando imagen de perfil: {str(e)}")
        return {
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        }
