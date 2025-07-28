"""
Utilidades adicionales para optimización de Cloudinary
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CloudinaryOptimizer:
    """Clase para optimizaciones avanzadas de Cloudinary"""
    
    def __init__(self):
        self.config = cloudinary.config()
    
    def get_optimized_url(self, public_id: str, width: int = None, height: int = None, 
                         quality: str = "auto", format: str = "auto") -> str:
        """
        Genera URL optimizada con transformaciones automáticas
        
        Args:
            public_id: ID público de la imagen en Cloudinary
            width: Ancho deseado (opcional)
            height: Alto deseado (opcional)
            quality: Calidad de la imagen (auto, 100, 90, etc.)
            format: Formato automático (auto, webp, jpg, png)
        
        Returns:
            URL optimizada
        """
        try:
            transformations = {
                'quality': quality,
                'fetch_format': format,
                'flags': 'progressive'  # Carga progresiva
            }
            
            if width:
                transformations['width'] = width
            if height:
                transformations['height'] = height
                transformations['crop'] = 'fill'  # Mantener aspect ratio
            
            url, _ = cloudinary.utils.cloudinary_url(
                public_id,
                **transformations
            )
            
            return url
            
        except Exception as e:
            logger.error(f"Error generando URL optimizada: {e}")
            return ""
    
    def get_responsive_urls(self, public_id: str) -> Dict[str, str]:
        """
        Genera URLs para diferentes tamaños responsive
        
        Args:
            public_id: ID público de la imagen
            
        Returns:
            Diccionario con URLs para diferentes tamaños
        """
        sizes = {
            'thumbnail': {'width': 150, 'height': 150},
            'small': {'width': 300, 'height': 300},
            'medium': {'width': 600, 'height': 600},
            'large': {'width': 1200, 'height': 1200},
            'original': {}
        }
        
        urls = {}
        for size_name, dimensions in sizes.items():
            urls[size_name] = self.get_optimized_url(public_id, **dimensions)
        
        return urls
    
    def get_usage_stats(self) -> Dict:
        """
        Obtiene estadísticas de uso de Cloudinary
        
        Returns:
            Diccionario con estadísticas de uso
        """
        try:
            usage = cloudinary.api.usage()
            return {
                'transformations': usage.get('transformations', 0),
                'objects': usage.get('objects', 0),
                'bandwidth': usage.get('bandwidth', 0),
                'storage': usage.get('storage', 0),
                'requests': usage.get('requests', 0),
                'plan': usage.get('plan', 'free'),
                'last_updated': usage.get('last_updated')
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def cleanup_unused_images(self, dry_run: bool = True) -> List[str]:
        """
        Identifica imágenes en Cloudinary que no están siendo usadas
        
        Args:
            dry_run: Si True, solo lista las imágenes sin eliminarlas
            
        Returns:
            Lista de public_ids de imágenes no utilizadas
        """
        try:
            # Obtener todas las imágenes de Cloudinary con prefijo de nuestra app
            cloudinary_images = cloudinary.api.resources(
                type="upload",
                prefix="tienda_sena/",
                max_results=500
            )
            
            # Obtener todos los public_ids en uso en la BD
            from tienda_sena.models import ImagenProducto
            public_ids_en_uso = set()
            
            for imagen in ImagenProducto.objects.exclude(imagen_cloudinary=''):
                if imagen.imagen_cloudinary:
                    # Extraer public_id de la URL de Cloudinary
                    public_id = self._extract_public_id(imagen.imagen_cloudinary)
                    if public_id:
                        public_ids_en_uso.add(public_id)
            
            # Identificar imágenes no utilizadas
            unused_images = []
            for resource in cloudinary_images.get('resources', []):
                public_id = resource['public_id']
                if public_id not in public_ids_en_uso:
                    unused_images.append(public_id)
                    
                    if not dry_run:
                        # Eliminar imagen de Cloudinary
                        cloudinary.uploader.destroy(public_id)
                        logger.info(f"Eliminada imagen no utilizada: {public_id}")
            
            return unused_images
            
        except Exception as e:
            logger.error(f"Error limpiando imágenes no utilizadas: {e}")
            return []
    
    def _extract_public_id(self, cloudinary_url: str) -> Optional[str]:
        """
        Extrae el public_id de una URL de Cloudinary
        
        Args:
            cloudinary_url: URL completa de Cloudinary
            
        Returns:
            public_id extraído o None si no se puede extraer
        """
        try:
            # Las URLs de Cloudinary tienen formato:
            # https://res.cloudinary.com/cloud_name/image/upload/v1234567890/public_id.jpg
            parts = cloudinary_url.split('/')
            if 'upload' in parts:
                upload_index = parts.index('upload')
                if len(parts) > upload_index + 2:
                    # Tomar la parte después de upload, saltando la versión si existe
                    public_id_part = '/'.join(parts[upload_index + 2:])
                    # Remover extensión de archivo
                    public_id = public_id_part.rsplit('.', 1)[0]
                    return public_id
            return None
        except Exception:
            return None

# Instancia global del optimizador
cloudinary_optimizer = CloudinaryOptimizer()
