"""
Comando de Django para migrar imágenes locales existentes a Cloudinary
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from tienda_sena.models import ImagenProducto
from tienda_sena.cloudinary_utils import cloudinary_manager
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Migra imágenes locales existentes a Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--producto-id',
            type=int,
            help='ID específico de producto para migrar (opcional)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecutar sin hacer cambios reales (solo simulación)',
        )
        parser.add_argument(
            '--max-imagenes',
            type=int,
            default=50,
            help='Máximo número de imágenes a migrar en esta ejecución',
        )

    def handle(self, *args, **options):
        producto_id = options.get('producto_id')
        dry_run = options.get('dry_run')
        max_imagenes = options.get('max_imagenes')

        self.stdout.write(
            self.style.SUCCESS(
                f'🚀 Iniciando migración de imágenes a Cloudinary'
            )
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('⚠️  MODO SIMULACIÓN - No se harán cambios reales')
            )

        # Filtrar imágenes que necesitan migración
        queryset = ImagenProducto.objects.filter(
            cloudinary_public_id__isnull=True,  # Sin ID de Cloudinary
            imagen__isnull=False               # Con imagen local
            # Removemos el filtro usa_cloudinary=False para incluir imágenes que necesitan migración
        )

        if producto_id:
            queryset = queryset.filter(producto__id=producto_id)
            self.stdout.write(f'🎯 Migrando solo producto ID: {producto_id}')

        # Limitar cantidad
        imagenes_a_migrar = queryset[:max_imagenes]
        total_imagenes = imagenes_a_migrar.count()

        if total_imagenes == 0:
            self.stdout.write(
                self.style.SUCCESS('✅ No hay imágenes que necesiten migración')
            )
            return

        self.stdout.write(f'📁 Encontradas {total_imagenes} imágenes para migrar')

        exitosas = 0
        fallidas = 0
        errores = []

        for imagen in imagenes_a_migrar:
            try:
                self.stdout.write(f'📤 Migrando imagen ID {imagen.id} del producto "{imagen.producto.nombre}"')
                
                if not dry_run:
                    # Realizar migración real
                    with transaction.atomic():
                        # Abrir archivo de imagen
                        imagen.imagen.open()
                        
                        # Subir a Cloudinary
                        resultado = cloudinary_manager.subir_imagen_producto(
                            imagen.imagen,
                            imagen.producto.id,
                            imagen.es_principal
                        )
                        
                        if resultado['success']:
                            # Actualizar registro en base de datos
                            imagen.cloudinary_public_id = resultado['public_id']
                            imagen.cloudinary_version = str(resultado['version'])
                            imagen.usa_cloudinary = True
                            imagen.save()
                            
                            exitosas += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'✅ Migrada exitosamente: {resultado["public_id"]}')
                            )
                            
                            # Mostrar información de optimización
                            metadata = resultado.get('metadata', {})
                            if metadata.get('bytes'):
                                mb_original = imagen.imagen.size / (1024 * 1024)
                                mb_cloudinary = metadata['bytes'] / (1024 * 1024)
                                ahorro = ((mb_original - mb_cloudinary) / mb_original * 100) if mb_original > 0 else 0
                                self.stdout.write(f'   💾 Optimización: {mb_original:.2f}MB → {mb_cloudinary:.2f}MB (Ahorro: {ahorro:.1f}%)')
                        else:
                            fallidas += 1
                            error_msg = f'Error subiendo imagen ID {imagen.id}'
                            errores.append(error_msg)
                            self.stdout.write(self.style.ERROR(f'❌ {error_msg}'))
                            
                else:
                    # Modo simulación
                    self.stdout.write(f'   🎭 SIMULACIÓN: Se migraría imagen "{imagen.imagen.name}"')
                    exitosas += 1

            except Exception as e:
                fallidas += 1
                error_msg = f'Error en imagen ID {imagen.id}: {str(e)}'
                errores.append(error_msg)
                self.stdout.write(self.style.ERROR(f'❌ {error_msg}'))
                logger.error(error_msg)

        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN DE MIGRACIÓN'))
        self.stdout.write('='*50)
        self.stdout.write(f'✅ Exitosas: {exitosas}')
        self.stdout.write(f'❌ Fallidas: {fallidas}')
        self.stdout.write(f'📊 Total procesadas: {exitosas + fallidas}')
        
        if errores:
            self.stdout.write('\n🚨 ERRORES ENCONTRADOS:')
            for error in errores[:5]:  # Mostrar solo los primeros 5
                self.stdout.write(f'   • {error}')
            if len(errores) > 5:
                self.stdout.write(f'   ... y {len(errores) - 5} errores más')

        if not dry_run and exitosas > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 Migración completada! {exitosas} imágenes ahora usan Cloudinary'
                )
            )

        # Estadísticas adicionales
        total_cloudinary = ImagenProducto.objects.filter(usa_cloudinary=True).count()
        total_local = ImagenProducto.objects.filter(usa_cloudinary=False).count()
        total_general = total_cloudinary + total_local

        if total_general > 0:
            porcentaje_cloudinary = (total_cloudinary / total_general) * 100
            self.stdout.write(f'\n📈 ESTADO ACTUAL DEL SISTEMA:')
            self.stdout.write(f'   ☁️  Cloudinary: {total_cloudinary} imágenes ({porcentaje_cloudinary:.1f}%)')
            self.stdout.write(f'   💾 Local: {total_local} imágenes ({100-porcentaje_cloudinary:.1f}%)')

        if not dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  RECOMENDACIÓN: Después de verificar que todo funciona correctamente, '
                    'puedes considerar eliminar las imágenes locales para ahorrar espacio.'
                )
            )
