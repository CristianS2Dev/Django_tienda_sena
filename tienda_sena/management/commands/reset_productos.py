import os
import shutil
import time
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from tienda_sena.models import Producto, ImagenProducto, Usuario, Categoria, Color

# Intentar importar CloudinaryManager, si no está disponible, continuar sin él
try:
    from tienda_sena.cloudinary_utils import CloudinaryManager
    CLOUDINARY_AVAILABLE = True
except ImportError as e:
    print(f"CloudinaryManager no disponible: {e}")
    CLOUDINARY_AVAILABLE = False


class Command(BaseCommand):
    help = 'Elimina todos los productos existentes y crea productos realistas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando limpieza de productos...'))
        
        # 1. Eliminar todas las imágenes de productos del media
        media_productos_path = os.path.join(settings.MEDIA_ROOT, 'productos')
        if os.path.exists(media_productos_path):
            shutil.rmtree(media_productos_path)
            self.stdout.write(self.style.SUCCESS('Imágenes de productos eliminadas'))
        
                # 2. Verificar directorio de imágenes por defecto
        imagenes_dir = os.path.join(
            settings.BASE_DIR, 
            'tienda_sena', 
            'static', 
            'assets', 
            'productos_default'
        )
        
        if not os.path.exists(imagenes_dir):
            self.stdout.write(
                self.style.WARNING(f'Directorio de imágenes no existe: {imagenes_dir}')
            )
            # Crear directorio si no existe
            os.makedirs(imagenes_dir, exist_ok=True)
            self.stdout.write(f'Directorio creado: {imagenes_dir}')
        
        # 3. Inicializar CloudinaryManager si está disponible
        cloudinary_manager = None
        if CLOUDINARY_AVAILABLE:
            try:
                cloudinary_manager = CloudinaryManager()
                self.stdout.write(self.style.SUCCESS('✓ CloudinaryManager inicializado'))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Error al inicializar CloudinaryManager: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ CloudinaryManager no disponible - solo se usará almacenamiento local')
            )
        
        # 4. Limpiar datos existentes
        ImagenProducto.objects.all().delete()
        Producto.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Productos eliminados de la base de datos'))
        
        # 5. Obtener vendedores (usuarios con rol vendedor o administrador)
        vendedores = Usuario.objects.filter(rol__in=[1, 3], activo=True)
        if not vendedores.exists():
            # Si no hay vendedores, crear uno por defecto
            vendedor = Usuario.objects.create(
                nombre_apellido="Vendedor Principal",
                documento="12345678",
                contacto=3001234567,
                correo="vendedor@tienda.com",
                password="password123",
                rol=3,
                activo=True
            )
            vendedores = [vendedor]
        
        # 4. Definir productos realistas con sus imágenes correspondientes
        productos_data = [
            {
                'nombre': 'Anillos Dorados Elegantes',
                'descripcion': 'Hermosos anillos dorados de alta calidad con acabado brillante. Perfectos para ocasiones especiales o uso diario elegante.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 4,      # Amarillo (como dorado)
                'precio': Decimal('280000'),
                'stock': 25,
                'en_oferta': True,
                'descuento': Decimal('15.00'),
                'imagenes': ['anillos_dorados.jpg']
            },
            {
                'nombre': 'Anillo con Diamante Premium',
                'descripcion': 'Anillo de compromiso con diamante genuino engastado en oro blanco. Diseño clásico y elegante para momentos especiales.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 2,      # Blanco
                'precio': Decimal('1800000'),
                'stock': 8,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['anillo_con_diamante.jpg']
            },
            {
                'nombre': 'Bolso Casual Moderno',
                'descripcion': 'Bolso versátil para uso diario con diseño moderno y práctico. Perfecto para estudiantes y profesionales.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 3,      # Negro/Gris
                'precio': Decimal('180000'),
                'stock': 20,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['bolso.webp']
            },
            {
                'nombre': 'Bolso Gucci Gris Elegante',
                'descripcion': 'Bolso de diseñador Gucci en color gris con acabados de lujo. Perfecto para mujeres que buscan elegancia y estilo.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 1,      # Gris
                'precio': Decimal('2400000'),
                'stock': 5,
                'en_oferta': True,
                'descuento': Decimal('20.00'),
                'imagenes': ['bolso_gucci_gris.jpg']
            },
            {
                'nombre': 'Bolso para Mujer Rojo',
                'descripcion': 'Bolso femenino en vibrante color rojo, ideal para complementar cualquier outfit. Amplio espacio interior y diseño moderno.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 6,      # Rojo
                'precio': Decimal('360000'),
                'stock': 15,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['bolso_mujer_rojo.jpg']
            },
            {
                'nombre': 'Bolso para Hombre Ejecutivo',
                'descripcion': 'Bolso masculino de cuero para ejecutivos. Diseño sofisticado con múltiples compartimentos para laptop y documentos.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 3,      # Negro
                'precio': Decimal('520000'),
                'stock': 12,
                'en_oferta': True,
                'descuento': Decimal('12.00'),
                'imagenes': ['bolso_para_hombre.jpg']
            },
            {
                'nombre': 'Brazalete de Plata Artesanal',
                'descripcion': 'Brazalete de plata 925 con diseño artesanal único. Perfecto para complementar cualquier estilo con elegancia.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 2,      # Blanco/Plata
                'precio': Decimal('240000'),
                'stock': 18,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['brazalete_de_plata.jpg']
            },
            {
                'nombre': 'Camibuso Azul Casual',
                'descripcion': 'Camibuso cómodo en color azul, perfecto para uso casual y deportivo. Material transpirable y de alta calidad.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('85000'),
                'stock': 30,
                'en_oferta': True,
                'descuento': Decimal('10.00'),
                'imagenes': ['camibuso_azul.jpg']
            },
            {
                'nombre': 'Camisa de Algodón Roja',
                'descripcion': 'Camisa de algodón 100% en vibrante color rojo. Corte clásico y cómodo para uso formal o casual.',
                'categoria': 2,  # Ropa
                'color': 6,      # Rojo
                'precio': Decimal('120000'),
                'stock': 20,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['camisa_algodon_roja.jpg']
            },
            {
                'nombre': 'Camisa Blanca Clásica',
                'descripcion': 'Camisa blanca de corte clásico, imprescindible en cualquier guardarropa. Ideal para ocasiones formales.',
                'categoria': 2,  # Ropa
                'color': 2,      # Blanco
                'precio': Decimal('95000'),
                'stock': 25,
                'en_oferta': True,
                'descuento': Decimal('8.00'),
                'imagenes': ['camisa_blanca.jpg']
            },
            {
                'nombre': 'Camisa para Hombre Blanca',
                'descripcion': 'Camisa masculina blanca de vestir con corte ejecutivo. Material premium y acabados de calidad.',
                'categoria': 2,  # Ropa
                'color': 2,      # Blanco
                'precio': Decimal('140000'),
                'stock': 18,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['camisa_para_hombre_blanca.jpg']
            },
            {
                'nombre': 'Canguro para Hombre Negro',
                'descripcion': 'Riñonera moderna para hombre en color negro. Perfecta para llevar elementos esenciales con estilo urbano.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 3,      # Negro
                'precio': Decimal('75000'),
                'stock': 22,
                'en_oferta': True,
                'descuento': Decimal('15.00'),
                'imagenes': ['cangurera_hombre_negro.webp']
            },
            {
                'nombre': 'Chaqueta Morada Elegante',
                'descripcion': 'Chaqueta en elegante color morado, perfecta para ocasiones especiales. Corte moderno y cómodo.',
                'categoria': 2,  # Ropa
                'color': 6,      # Rojo (más cercano disponible)
                'precio': Decimal('380000'),
                'stock': 10,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['chaqueta_morada.jpg']
            },
            {
                'nombre': 'Chaqueta Negra Versátil',
                'descripcion': 'Chaqueta negra versátil que combina con cualquier outfit. Ideal para uso formal o casual elegante.',
                'categoria': 2,  # Ropa
                'color': 3,      # Negro
                'precio': Decimal('420000'),
                'stock': 15,
                'en_oferta': True,
                'descuento': Decimal('18.00'),
                'imagenes': ['chaqueta_negra.jpg']
            },
            {
                'nombre': 'Conjunto Camisa y Zapatos',
                'descripcion': 'Conjunto completo de camisa y zapatos formales. Perfecto para eventos especiales y uso ejecutivo.',
                'categoria': 2,  # Ropa
                'color': 2,      # Blanco
                'precio': Decimal('680000'),
                'stock': 8,
                'en_oferta': True,
                'descuento': Decimal('25.00'),
                'imagenes': ['conjunto_camisa_zapatos.jpg']
            },
            {
                'nombre': 'Disco Portátil 1TB',
                'descripcion': 'Disco duro portátil de 1TB con alta velocidad de transferencia. Ideal para almacenamiento y backup de datos.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('280000'),
                'stock': 30,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['disco_portable_1tb.jpg']
            },
            {
                'nombre': 'Jeans Mixtos Modernos',
                'descripcion': 'Jeans de diseño moderno con corte unisex. Perfectos para looks casuales y cómodos.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('150000'),
                'stock': 25,
                'en_oferta': True,
                'descuento': Decimal('8.00'),
                'imagenes': ['jeans_mixtos.jpg']
            },
            {
                'nombre': 'Jean para Hombre Clásico',
                'descripcion': 'Jean masculino de corte clásico en denim de alta calidad. Cómodo y duradero para uso diario.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('160000'),
                'stock': 25,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['jean_hombre.jpg']
            },
            {
                'nombre': 'Jean Mixto Unisex',
                'descripcion': 'Jean de diseño unisex en denim premium. Corte moderno que se adapta a diferentes estilos.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('180000'),
                'stock': 20,
                'en_oferta': True,
                'descuento': Decimal('12.00'),
                'imagenes': ['jean_mixto.jpg']
            },
            {
                'nombre': 'Jean para Mujer Elegante',
                'descripcion': 'Jean femenino con corte elegante y cómodo. Diseño moderno que realza la figura femenina.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('170000'),
                'stock': 22,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['jean_mujer.jpg']
            },
            {
                'nombre': 'Jean Mujer Azul Premium',
                'descripcion': 'Jean femenino en denim azul premium con acabados de calidad. Perfecto para uso casual elegante.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('195000'),
                'stock': 18,
                'en_oferta': True,
                'descuento': Decimal('10.00'),
                'imagenes': ['jean_mujer_azul.jpg']
            },
            {
                'nombre': 'Monitor Acer 22 Pulgadas',
                'descripcion': 'Monitor Acer de 22 pulgadas con resolución Full HD. Perfecto para trabajo, gaming y entretenimiento.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('680000'),
                'stock': 15,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['pantalla_acer_22.jpg']
            },
            {
                'nombre': 'Monitor Curvo Gaming',
                'descripcion': 'Monitor curvo para gaming con alta frecuencia de actualización. Experiencia inmersiva para jugadores.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('1200000'),
                'stock': 10,
                'en_oferta': True,
                'descuento': Decimal('20.00'),
                'imagenes': ['pantalla_curba.jpg']
            },
            {
                'nombre': 'Pulsera Plateada Dragón',
                'descripcion': 'Pulsera de plata con diseño de dragón artesanal. Accesorio único con simbolismo oriental.',
                'categoria': 2,  # Ropa/Accesorios
                'color': 2,      # Blanco/Plata
                'precio': Decimal('320000'),
                'stock': 12,
                'en_oferta': True,
                'descuento': Decimal('15.00'),
                'imagenes': ['pulsera_plateada_dragon.jpg']
            },
            {
                'nombre': 'SSD 1TB Alta Velocidad',
                'descripcion': 'Disco sólido SSD de 1TB con velocidades de lectura ultrarrápidas. Mejora el rendimiento de tu equipo.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('450000'),
                'stock': 20,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['ssd_1tb.jpg']
            },
            {
                'nombre': 'SSD 500GB Compacto',
                'descripcion': 'Disco sólido SSD de 500GB en formato compacto. Ideal para laptops y sistemas de escritorio.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('250000'),
                'stock': 25,
                'en_oferta': True,
                'descuento': Decimal('12.00'),
                'imagenes': ['ssd_500.jpg']
            }
        ]
        
        # 5. Crear productos con imágenes
        productos_creados = 0
        imagenes_creadas = 0
        errores_cloudinary = 0
        
        for producto_data in productos_data:
            try:
                # Extraer las imágenes de los datos del producto
                imagenes_nombres = producto_data.pop('imagenes', [])
                
                # Agregar vendedor aleatorio
                vendedor = random.choice(list(vendedores))
                producto_data['vendedor'] = vendedor
                producto_data['precio_original'] = producto_data.pop('precio')
                
                # Crear el producto
                producto = Producto.objects.create(**producto_data)
                productos_creados += 1
                
                # Crear imágenes para este producto
                for orden, imagen_nombre in enumerate(imagenes_nombres):
                    imagen_path = os.path.join(imagenes_dir, imagen_nombre)
                    
                    if os.path.exists(imagen_path):
                        try:
                            # Crear objeto ImagenProducto
                            imagen_producto = ImagenProducto(
                                producto=producto,
                                orden=orden,
                                es_principal=(orden == 0)
                            )
                            
                            # Intentar subir a Cloudinary primero (si está disponible)
                            cloudinary_success = False
                            if cloudinary_manager:
                                try:
                                    result = cloudinary_manager.upload_image(
                                        imagen_path,
                                        folder='productos',
                                        public_id=f'producto_{producto.id}_{orden}_{int(time.time())}'
                                    )
                                    
                                    if result and result.get('public_id'):
                                        imagen_producto.cloudinary_public_id = result['public_id']
                                        cloudinary_success = True
                                        self.stdout.write(
                                            self.style.SUCCESS(
                                                f'  ✓ Subido a Cloudinary: {imagen_nombre} -> {result["public_id"]}'
                                            )
                                        )
                                    else:
                                        errores_cloudinary += 1
                                        self.stdout.write(
                                            self.style.WARNING(
                                                f'  ⚠ Cloudinary no devolvió public_id para {imagen_nombre}'
                                            )
                                        )
                                        
                                except Exception as cloudinary_error:
                                    errores_cloudinary += 1
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f'  ⚠ Error Cloudinary para {imagen_nombre}: {str(cloudinary_error)}'
                                        )
                                    )
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'  ⚠ CloudinaryManager no disponible para {imagen_nombre}'
                                    )
                                )
                            
                            # Siempre guardar copia local como respaldo
                            with open(imagen_path, 'rb') as img_file:
                                imagen_producto.imagen.save(
                                    imagen_nombre,
                                    ContentFile(img_file.read()),
                                    save=False
                                )
                            
                            imagen_producto.save()
                            imagenes_creadas += 1
                            
                            status_msg = f'  ✓ Imagen creada: {imagen_nombre} para {producto.nombre}'
                            if cloudinary_success:
                                status_msg += ' (Cloudinary + Local)'
                            else:
                                status_msg += ' (Solo Local)'
                            
                            self.stdout.write(self.style.SUCCESS(status_msg))
                            
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  ⚠ Error al procesar imagen {imagen_nombre}: {str(e)}'
                                )
                            )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'  ⚠ Imagen no encontrada: {imagen_path}'
                            )
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Producto creado: {producto.nombre}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error al crear producto {producto_data.get("nombre", "desconocido")}: {str(e)}'
                    )
                )

        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'¡Proceso completado exitosamente!'))
        self.stdout.write('='*50)
        
        # Estadísticas detalladas
        self.stdout.write('\n--- ESTADÍSTICAS ---')
        self.stdout.write(f'✓ Productos creados: {productos_creados}')
        self.stdout.write(f'✓ Imágenes procesadas: {imagenes_creadas}')
        if errores_cloudinary > 0:
            self.stdout.write(f'⚠ Errores de Cloudinary: {errores_cloudinary}')
        
        # Resumen de base de datos
        self.stdout.write('\n--- RESUMEN DE BASE DE DATOS ---')
        total_productos = Producto.objects.count()
        productos_oferta = Producto.objects.filter(en_oferta=True).count()
        total_imagenes = ImagenProducto.objects.count()
        imagenes_cloudinary = ImagenProducto.objects.exclude(cloudinary_public_id__isnull=True).exclude(cloudinary_public_id__exact='').count()
        
        self.stdout.write(f'Total de productos: {total_productos}')
        self.stdout.write(f'Productos en oferta: {productos_oferta}')
        self.stdout.write(f'Total de imágenes: {total_imagenes}')
        self.stdout.write(f'Imágenes en Cloudinary: {imagenes_cloudinary}')
        
        # Mostrar distribución por categorías
        self.stdout.write('\n--- DISTRIBUCIÓN POR CATEGORÍAS ---')
        for categoria in Categoria.objects.all():
            count = Producto.objects.filter(categoria=categoria).count()
            if count > 0:
                self.stdout.write(f'{categoria.nombre}: {count} productos')
        
        self.stdout.write('\n✨ ¡Todos los productos han sido creados con éxito!')
