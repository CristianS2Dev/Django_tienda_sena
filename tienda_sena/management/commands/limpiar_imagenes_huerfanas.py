"""
Comando para limpiar imágenes huérfanas y sin archivos
"""
from django.core.management.base import BaseCommand
from django.db import models
from tienda_sena.models import ImagenProducto, Producto
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Limpia imágenes huérfanas y registros sin archivos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Solo muestra lo que se haría, sin hacer cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write("🧹 Iniciando limpieza de imágenes...")
        
        # 1. Buscar imágenes sin archivo local
        imagenes_sin_archivo = ImagenProducto.objects.filter(imagen='')
        
        self.stdout.write(f"📋 Encontradas {imagenes_sin_archivo.count()} imágenes sin archivo local")
        
        for imagen in imagenes_sin_archivo:
            if imagen.imagen_cloudinary:
                self.stdout.write(f"   ✅ ID {imagen.id}: Tiene Cloudinary, mantener")
            else:
                if not dry_run:
                    imagen.delete()
                    self.stdout.write(f"   🗑️ ID {imagen.id}: Eliminada (sin archivo local ni Cloudinary)")
                else:
                    self.stdout.write(f"   🗑️ ID {imagen.id}: Se eliminaría (sin archivo local ni Cloudinary)")
        
        # 2. Buscar imágenes huérfanas (sin producto)
        imagenes_huerfanas = ImagenProducto.objects.filter(producto__isnull=True)
        
        self.stdout.write(f"📋 Encontradas {imagenes_huerfanas.count()} imágenes huérfanas")
        
        for imagen in imagenes_huerfanas:
            if not dry_run:
                imagen.delete()
                self.stdout.write(f"   🗑️ ID {imagen.id}: Eliminada (sin producto asociado)")
            else:
                self.stdout.write(f"   🗑️ ID {imagen.id}: Se eliminaría (sin producto asociado)")
        
        # 3. Buscar archivos locales sin registro en BD
        if os.path.exists(settings.MEDIA_ROOT):
            productos_dir = os.path.join(settings.MEDIA_ROOT, 'productos')
            if os.path.exists(productos_dir):
                archivos_locales = []
                for root, dirs, files in os.walk(productos_dir):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                            archivo_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
                            archivos_locales.append(archivo_path)
                
                self.stdout.write(f"📋 Encontrados {len(archivos_locales)} archivos locales de productos")
                
                archivos_huerfanos = 0
                for archivo in archivos_locales:
                    # Buscar si existe un registro que use este archivo
                    existe_registro = ImagenProducto.objects.filter(
                        models.Q(imagen=archivo) | 
                        models.Q(imagen_original=archivo) | 
                        models.Q(miniatura=archivo)
                    ).exists()
                    
                    if not existe_registro:
                        archivos_huerfanos += 1
                        archivo_completo = os.path.join(settings.MEDIA_ROOT, archivo)
                        if not dry_run:
                            try:
                                os.remove(archivo_completo)
                                self.stdout.write(f"   🗑️ Eliminado archivo: {archivo}")
                            except OSError:
                                self.stdout.write(f"   ❌ Error eliminando: {archivo}")
                        else:
                            self.stdout.write(f"   🗑️ Se eliminaría archivo: {archivo}")
                
                self.stdout.write(f"📋 {archivos_huerfanos} archivos huérfanos encontrados")
        
        if dry_run:
            self.stdout.write("✅ Simulación completada. Usa --no-dry-run para aplicar cambios")
        else:
            self.stdout.write("✅ Limpieza completada")
