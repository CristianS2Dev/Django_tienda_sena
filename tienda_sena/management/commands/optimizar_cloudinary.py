"""
Comando para obtener estad        # 1. Estadísticas de uso
        stats = cloudinary_optimizer.get_usage_stats()
        if stats:
            self.stdout.write(f"☁️ Plan: {stats.get('plan', 'Unknown')}")
            self.stdout.write(f"📁 Objetos almacenados: {stats.get('objects', 0)}")
            self.stdout.write(f"🔄 Transformaciones: {stats.get('transformations', 0)}")
            self.stdout.write(f"📊 Ancho de banda usado: {stats.get('bandwidth', 0)} bytes")
            self.stdout.write(f"💾 Storage usado: {stats.get('storage', 0)} bytes")
            self.stdout.write(f"🔗 Requests: {stats.get('requests', 0)}") optimizar el uso de Cloudinary
"""
from django.core.management.base import BaseCommand
from tienda_sena.models import ImagenProducto, Producto
from tienda_sena.cloudinary_optimizer import cloudinary_optimizer
import cloudinary.api

class Command(BaseCommand):
    help = 'Obtiene estadísticas y optimiza el uso de Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Limpia imágenes no utilizadas de Cloudinary',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Solo muestra lo que se haría, sin hacer cambios',
        )

    def handle(self, *args, **options):
        cleanup = options['cleanup']
        dry_run = options['dry_run']
        
        self.stdout.write("📊 ESTADÍSTICAS DE CLOUDINARY")
        self.stdout.write("=" * 50)
        
        # 1. Estadísticas de uso
        stats = cloudinary_optimizer.get_usage_stats()
        if stats:
            self.stdout.write(f"☁️ Plan: {stats.get('plan', 'Unknown')}")
            self.stdout.write(f"📁 Objetos almacenados: {stats.get('objects', 0)}")
            self.stdout.write(f"🔄 Transformaciones: {stats.get('transformations', 0)}")
            self.stdout.write(f"📊 Ancho de banda usado: {stats.get('bandwidth', 0)} bytes")
            self.stdout.write(f"💾 Storage usado: {stats.get('storage', 0)} bytes")
            self.stdout.write(f"🔗 Requests: {stats.get('requests', 0)}")
        
        # 2. Estadísticas de base de datos
        self.stdout.write("\n📋 ESTADÍSTICAS DE BASE DE DATOS")
        self.stdout.write("=" * 50)
        
        total_imagenes = ImagenProducto.objects.count()
        imagenes_cloudinary = ImagenProducto.objects.exclude(imagen_cloudinary='').count()
        imagenes_con_archivo_local = ImagenProducto.objects.exclude(imagen='').count()
        imagenes_huerfanas = ImagenProducto.objects.filter(producto__isnull=True).count()
        
        self.stdout.write(f"📊 Total de imágenes en BD: {total_imagenes}")
        self.stdout.write(f"☁️ En Cloudinary: {imagenes_cloudinary}")
        self.stdout.write(f"💾 Con archivo local: {imagenes_con_archivo_local}")
        self.stdout.write(f"🗑️ Registros huérfanos: {imagenes_huerfanas}")
        
        if total_imagenes > 0:
            porcentaje_cloudinary = (imagenes_cloudinary / total_imagenes) * 100
            self.stdout.write(f"📈 Progreso migración: {porcentaje_cloudinary:.1f}%")
        
        # 3. Análisis por producto
        self.stdout.write("\n📦 ANÁLISIS POR PRODUCTO")
        self.stdout.write("=" * 50)
        
        productos_con_imagenes = Producto.objects.filter(imagenes__isnull=False).distinct()
        productos_completamente_migrados = 0
        productos_parcialmente_migrados = 0
        productos_sin_migrar = 0
        
        for producto in productos_con_imagenes:
            imagenes_producto = producto.imagenes.all()
            cloudinary_count = imagenes_producto.exclude(imagen_cloudinary='').count()
            total_count = imagenes_producto.count()
            
            if cloudinary_count == total_count:
                productos_completamente_migrados += 1
            elif cloudinary_count > 0:
                productos_parcialmente_migrados += 1
            else:
                productos_sin_migrar += 1
        
        self.stdout.write(f"✅ Productos completamente migrados: {productos_completamente_migrados}")
        self.stdout.write(f"⚠️ Productos parcialmente migrados: {productos_parcialmente_migrados}")
        self.stdout.write(f"❌ Productos sin migrar: {productos_sin_migrar}")
        
        # 4. Limpieza de imágenes no utilizadas
        if cleanup:
            self.stdout.write("\n🧹 LIMPIEZA DE CLOUDINARY")
            self.stdout.write("=" * 50)
            
            unused_images = cloudinary_optimizer.cleanup_unused_images(dry_run=dry_run)
            
            if unused_images:
                self.stdout.write(f"🗑️ Encontradas {len(unused_images)} imágenes no utilizadas:")
                for public_id in unused_images:
                    action = "Se eliminaría" if dry_run else "Eliminada"
                    self.stdout.write(f"   {action}: {public_id}")
            else:
                self.stdout.write("✅ No se encontraron imágenes no utilizadas")
        
        # 5. Recomendaciones
        self.stdout.write("\n💡 RECOMENDACIONES")
        self.stdout.write("=" * 50)
        
        if imagenes_cloudinary < total_imagenes:
            pendientes = total_imagenes - imagenes_cloudinary
            self.stdout.write(f"🔄 Migrar {pendientes} imágenes restantes:")
            self.stdout.write("   python manage.py migrar_a_cloudinary")
        
        if imagenes_huerfanas > 0:
            self.stdout.write(f"🧹 Limpiar {imagenes_huerfanas} registros huérfanos:")
            self.stdout.write("   python manage.py limpiar_imagenes_huerfanas")
        
        # Sugerencias de optimización
        self.stdout.write("📈 Optimizaciones recomendadas:")
        self.stdout.write("   - Usar filtros cloudinary_responsive en templates")
        self.stdout.write("   - Implementar lazy loading con cloudinary_picture")
        self.stdout.write("   - Configurar transformaciones automáticas")
        self.stdout.write("   - Activar formato WebP automático")
        
        # Alertas de límites
        if stats:
            transformations = stats.get('transformations', 0)
            plan = stats.get('plan', 'free')
            
            if plan == 'free' and transformations > 20000:
                self.stdout.write("⚠️ ALERTA: Cerca del límite de transformaciones del plan gratuito")
            
            bandwidth = stats.get('bandwidth', 0)
            if plan == 'free' and bandwidth > 20000000000:  # 20GB
                self.stdout.write("⚠️ ALERTA: Cerca del límite de ancho de banda")
        
        self.stdout.write("\n✅ Análisis completado")
