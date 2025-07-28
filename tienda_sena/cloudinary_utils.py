"""
Utilidades para el manejo de Cloudinary en el proyecto Tienda SENA
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.exceptions import ValidationError
import uuid
from typing import Dict, Any, Optional
import logging

# Configurar logging
logger = logging.getLogger(__name__)

class CloudinaryManager:
    """
    Clase para gestionar todas las operaciones con Cloudinary.
    Centraliza la lógica de subida, transformación y eliminación de imágenes.
    """
    
    def __init__(self):
        """
        Inicializa el manager con configuraciones predefinidas para la tienda.
        """
        # Configuraciones por defecto para productos
        self.PRODUCTO_CONFIG = {
            'folder': 'tienda_sena/productos',
            'quality': 'auto',
            'fetch_format': 'auto',
            'allowed_formats': ['jpg', 'jpeg', 'png', 'webp'],
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'transformations': {
                'optimizada': {'width': 800, 'height': 800, 'crop': 'limit'},
                'miniatura': {'width': 300, 'height': 300, 'crop': 'fill'},
                'banner': {'width': 1200, 'height': 400, 'crop': 'fill'},
                'zoom': {'width': 1500, 'height': 1500, 'crop': 'limit'}
            }
        }
        
        # Configuraciones para perfiles de usuario
        self.PERFIL_CONFIG = {
            'folder': 'tienda_sena/perfiles',
            'quality': 'auto',
            'fetch_format': 'auto',
            'allowed_formats': ['jpg', 'jpeg', 'png'],
            'max_file_size': 5 * 1024 * 1024,  # 5MB
            'transformations': {
                'optimizada': {'width': 300, 'height': 300, 'crop': 'fill', 'gravity': 'face'},
                'miniatura': {'width': 150, 'height': 150, 'crop': 'fill', 'gravity': 'face'}
            }
        }

    def validar_imagen(self, archivo, config_tipo: str = 'producto') -> None:
        """
        Valida que la imagen cumpla con los requisitos.
        
        Args:
            archivo: Archivo de imagen a validar
            config_tipo: Tipo de configuración ('producto' o 'perfil')
        
        Raises:
            ValidationError: Si la imagen no cumple los requisitos
        """
        config = self.PRODUCTO_CONFIG if config_tipo == 'producto' else self.PERFIL_CONFIG
        
        if not archivo:
            raise ValidationError("No se proporcionó ningún archivo.")
        
        # Validar extensión
        extension = archivo.name.lower().split('.')[-1] if '.' in archivo.name else ''
        if extension not in config['allowed_formats']:
            raise ValidationError(
                f"Formato no permitido. Use: {', '.join(config['allowed_formats'])}"
            )
        
        # Validar tamaño
        if archivo.size > config['max_file_size']:
            max_mb = config['max_file_size'] / (1024 * 1024)
            raise ValidationError(f"El archivo es muy grande. Máximo {max_mb}MB permitido.")
        
        # Validar tamaño mínimo
        if archivo.size < 1024:  # 1KB mínimo
            raise ValidationError("El archivo es demasiado pequeño.")

    def subir_imagen_producto(self, archivo, producto_id: int, es_principal: bool = False) -> Dict[str, Any]:
        """
        Sube una imagen de producto a Cloudinary con transformaciones automáticas.
        
        Args:
            archivo: Archivo de imagen
            producto_id: ID del producto
            es_principal: Si es la imagen principal del producto
        
        Returns:
            Dict con información de la imagen subida
        """
        try:
            # Validar imagen
            self.validar_imagen(archivo, 'producto')
            
            # Generar ID único para la imagen
            unique_id = str(uuid.uuid4())[:8]
            public_id = f"producto_{producto_id}_{unique_id}"
            
            # Configurar transformaciones para subida
            transformaciones = [
                self.PRODUCTO_CONFIG['transformations']['optimizada'],
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
            
            # Subir imagen principal con transformaciones
            resultado = cloudinary.uploader.upload(
                archivo,
                public_id=public_id,
                folder=self.PRODUCTO_CONFIG['folder'],
                transformation=transformaciones,
                overwrite=True,
                resource_type="image",
                tags=[f"producto_{producto_id}", "tienda_sena"]
            )
            
            # Generar URLs para diferentes tamaños
            urls = self._generar_urls_producto(resultado['public_id'])
            
            return {
                'success': True,
                'public_id': resultado['public_id'],
                'version': resultado['version'],
                'urls': urls,
                'metadata': {
                    'width': resultado.get('width'),
                    'height': resultado.get('height'),
                    'format': resultado.get('format'),
                    'bytes': resultado.get('bytes'),
                    'url_original': resultado['secure_url']
                }
            }
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error subiendo imagen de producto: {str(e)}")
            raise ValidationError(f"Error al subir imagen: {str(e)}")

    def subir_imagen_perfil(self, archivo, usuario_id: int) -> Dict[str, Any]:
        """
        Sube una imagen de perfil a Cloudinary.
        
        Args:
            archivo: Archivo de imagen
            usuario_id: ID del usuario
        
        Returns:
            Dict con información de la imagen subida
        """
        try:
            # Validar imagen
            self.validar_imagen(archivo, 'perfil')
            
            # ID único para el perfil
            public_id = f"perfil_{usuario_id}"
            
            # Configurar transformaciones para perfil (circular, optimizada)
            transformaciones = [
                self.PERFIL_CONFIG['transformations']['optimizada'],
                {'quality': 'auto', 'fetch_format': 'auto'}
            ]
            
            # Subir imagen de perfil
            resultado = cloudinary.uploader.upload(
                archivo,
                public_id=public_id,
                folder=self.PERFIL_CONFIG['folder'],
                transformation=transformaciones,
                overwrite=True,
                resource_type="image",
                tags=[f"usuario_{usuario_id}", "perfil", "tienda_sena"]
            )
            
            # Generar URLs para perfil
            urls = self._generar_urls_perfil(resultado['public_id'])
            
            return {
                'success': True,
                'public_id': resultado['public_id'],
                'version': resultado['version'],
                'urls': urls,
                'metadata': {
                    'width': resultado.get('width'),
                    'height': resultado.get('height'),
                    'format': resultado.get('format'),
                    'bytes': resultado.get('bytes'),
                    'url_original': resultado['secure_url']
                }
            }
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error subiendo imagen de perfil: {str(e)}")
            raise ValidationError(f"Error al subir imagen de perfil: {str(e)}")

    def _generar_urls_producto(self, public_id: str) -> Dict[str, str]:
        """
        Genera URLs optimizadas para diferentes usos del producto.
        
        Args:
            public_id: ID público de la imagen en Cloudinary
        
        Returns:
            Dict con URLs para diferentes tamaños
        """
        return {
            'optimizada': cloudinary.CloudinaryImage(public_id).build_url(**self.PRODUCTO_CONFIG['transformations']['optimizada']),
            'miniatura': cloudinary.CloudinaryImage(public_id).build_url(**self.PRODUCTO_CONFIG['transformations']['miniatura']),
            'banner': cloudinary.CloudinaryImage(public_id).build_url(**self.PRODUCTO_CONFIG['transformations']['banner']),
            'zoom': cloudinary.CloudinaryImage(public_id).build_url(**self.PRODUCTO_CONFIG['transformations']['zoom']),
            'original': cloudinary.CloudinaryImage(public_id).build_url()
        }

    def _generar_urls_perfil(self, public_id: str) -> Dict[str, str]:
        """
        Genera URLs optimizadas para imagen de perfil.
        
        Args:
            public_id: ID público de la imagen en Cloudinary
        
        Returns:
            Dict con URLs para diferentes tamaños de perfil
        """
        return {
            'optimizada': cloudinary.CloudinaryImage(public_id).build_url(**self.PERFIL_CONFIG['transformations']['optimizada']),
            'miniatura': cloudinary.CloudinaryImage(public_id).build_url(**self.PERFIL_CONFIG['transformations']['miniatura']),
            'original': cloudinary.CloudinaryImage(public_id).build_url()
        }

    def eliminar_imagen(self, public_id: str) -> bool:
        """
        Elimina una imagen de Cloudinary.
        
        Args:
            public_id: ID público de la imagen a eliminar
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            resultado = cloudinary.uploader.destroy(public_id)
            return resultado.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Error eliminando imagen {public_id}: {str(e)}")
            return False

    def obtener_info_imagen(self, public_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información detallada de una imagen en Cloudinary.
        
        Args:
            public_id: ID público de la imagen
        
        Returns:
            Dict con información de la imagen o None si no existe
        """
        try:
            resultado = cloudinary.api.resource(public_id)
            return {
                'public_id': resultado['public_id'],
                'format': resultado['format'],
                'width': resultado['width'],
                'height': resultado['height'],
                'bytes': resultado['bytes'],
                'created_at': resultado['created_at'],
                'url': resultado['secure_url']
            }
        except Exception as e:
            logger.warning(f"No se pudo obtener info de imagen {public_id}: {str(e)}")
            return None


# Instancia global del manager para usar en todo el proyecto
cloudinary_manager = CloudinaryManager()
