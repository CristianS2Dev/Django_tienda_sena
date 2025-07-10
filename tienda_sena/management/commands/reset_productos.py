import os
import shutil
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from tienda_sena.models import Producto, ImagenProducto, Usuario
import random


class Command(BaseCommand):
    help = 'Elimina todos los productos existentes y crea productos realistas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando limpieza de productos...'))
        
        # 1. Eliminar todas las imágenes de productos del media
        media_productos_path = os.path.join(settings.MEDIA_ROOT, 'productos')
        if os.path.exists(media_productos_path):
            shutil.rmtree(media_productos_path)
            self.stdout.write(self.style.SUCCESS('Imágenes de productos eliminadas'))
        
        # 2. Eliminar todos los productos de la base de datos
        ImagenProducto.objects.all().delete()
        Producto.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Productos eliminados de la base de datos'))
        
        # 3. Obtener vendedores (usuarios con rol vendedor o administrador)
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
                'nombre': 'Zapatillas Deportivas Nike',
                'descripcion': 'Zapatillas deportivas de alta calidad para running y entrenamiento. Suela antideslizante y diseño ergonómico.',
                'categoria': 4,  # Deportes
                'color': 3,      # Negro
                'precio': Decimal('129.99'),
                'stock': 25,
                'en_oferta': True,
                'descuento': Decimal('15.00'),
                'imagenes': ['51Y5NI-I5jL._AC_UX679_.jpg']
            },
            {
                'nombre': 'Bolso de Cuero Elegante',
                'descripcion': 'Bolso de cuero genuino para mujer, perfecto para el día a día. Incluye múltiples compartimentos.',
                'categoria': 2,  # Ropa
                'color': 1,      # Gris
                'precio': Decimal('89.99'),
                'stock': 15,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['bolso.webp']
            },
            {
                'nombre': 'Smartwatch Fitness Tracker',
                'descripcion': 'Reloj inteligente con monitor de frecuencia cardíaca, GPS y resistencia al agua. Batería de 7 días.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('199.99'),
                'stock': 20,
                'en_oferta': True,
                'descuento': Decimal('25.00'),
                'imagenes': ['61U7T1koQqL._AC_SX679_.jpg']
            },
            {
                'nombre': 'Mochila de Viaje',
                'descripcion': 'Mochila resistente al agua con múltiples compartimentos. Ideal para viajes y aventuras.',
                'categoria': 4,  # Deportes
                'color': 2,      # Blanco
                'precio': Decimal('75.50'),
                'stock': 30,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['51eg55uWmdL._AC_UX679_.jpg']
            },
            {
                'nombre': 'Auriculares Bluetooth Premium',
                'descripcion': 'Auriculares inalámbricos con cancelación de ruido activa. Sonido de alta fidelidad y 30 horas de batería.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('159.99'),
                'stock': 18,
                'en_oferta': True,
                'descuento': Decimal('20.00'),
                'imagenes': ['61pHAEJ4NML_sqBwShn._AC_UX679_.jpg']
            },
            {
                'nombre': 'Chaqueta de Invierno',
                'descripcion': 'Chaqueta térmica resistente al viento y al agua. Perfecta para temperaturas extremas.',
                'categoria': 2,  # Ropa
                'color': 3,      # Negro
                'precio': Decimal('120.00'),
                'stock': 12,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['71HblAHs5xL_YIiaiRb._AC_UY879_-2.jpg']
            },
            {
                'nombre': 'Set de Utensilios de Cocina',
                'descripcion': 'Juego completo de utensilios de cocina de acero inoxidable. Incluye 12 piezas esenciales.',
                'categoria': 3,  # Hogar
                'color': 2,      # Blanco
                'precio': Decimal('65.99'),
                'stock': 22,
                'en_oferta': True,
                'descuento': Decimal('10.00'),
                'imagenes': ['61mtL65D4cL_uyxIC28_A1Gjj7j._AC_SX679_.jpg']
            },
            {
                'nombre': 'Laptop Gaming HP',
                'descripcion': 'Laptop para gaming con procesador Intel i7, 16GB RAM, tarjeta gráfica GTX 1660Ti y SSD de 512GB.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('899.99'),
                'stock': 8,
                'en_oferta': True,
                'descuento': Decimal('12.00'),
                'imagenes': ['81QpkIctqPL._AC_SX679_.jpg']
            },
            {
                'nombre': 'Juego de Sábanas Premium',
                'descripcion': 'Juego de sábanas de algodón egipcio 100%. Suaves, cómodas y duraderas. Incluye funda de almohada.',
                'categoria': 3,  # Hogar
                'color': 2,      # Blanco
                'precio': Decimal('45.99'),
                'stock': 35,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['61sbMiUnoGL._AC_UL640_QL65_ML3_.jpg']
            },
            {
                'nombre': 'Cámara Digital Profesional',
                'descripcion': 'Cámara DSLR con lente 18-55mm, sensor de 24MP y grabación de video 4K. Perfecta para fotografía profesional.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('549.99'),
                'stock': 10,
                'en_oferta': True,
                'descuento': Decimal('18.00'),
                'imagenes': ['jason-leung-EtOMMg1nSR8-unsplash.jpg']
            },
            {
                'nombre': 'Vestido Casual Elegante',
                'descripcion': 'Vestido de algodón para uso diario. Cómodo, elegante y disponible en varios talles.',
                'categoria': 2,  # Ropa
                'color': 5,      # Azul
                'precio': Decimal('39.99'),
                'stock': 28,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['71YXzeOuslL_UYgtuLN._AC_UY879_.jpg']
            },
            {
                'nombre': 'Perfume Unisex Luxury',
                'descripcion': 'Fragancia premium unisex con notas frescas y duraderas. Presentación de 100ml.',
                'categoria': 8,  # Salud y Belleza
                'color': 0,      # Ninguno
                'precio': Decimal('85.00'),
                'stock': 16,
                'en_oferta': True,
                'descuento': Decimal('22.00'),
                'imagenes': ['content-pixie-ZB4eQcNqVUs-unsplash.jpg']
            },
            {
                'nombre': 'Teclado Mecánico Gaming',
                'descripcion': 'Teclado mecánico RGB para gaming con switches Cherry MX. Retroiluminación personalizable.',
                'categoria': 1,  # Electrónicos
                'color': 3,      # Negro
                'precio': Decimal('119.99'),
                'stock': 14,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['81Zt42ioCgL._AC_SX679_.jpg']
            },
            {
                'nombre': 'Plantas Decorativas de Interior',
                'descripcion': 'Set de 3 plantas ideales para decorar espacios interiores. Fáciles de cuidar y purificadoras de aire.',
                'categoria': 9,  # Jardín
                'color': 0,      # Ninguno
                'precio': Decimal('32.50'),
                'stock': 25,
                'en_oferta': True,
                'descuento': Decimal('8.00'),
                'imagenes': ['arno-senoner-oCXVxwTFwqE-unsplash.jpg']
            },
            {
                'nombre': 'Reloj de Pulsera Clásico',
                'descripcion': 'Reloj analógico de pulsera con correa de cuero genuino. Diseño clásico y elegante.',
                'categoria': 2,  # Ropa (accesorios)
                'color': 1,      # Gris
                'precio': Decimal('95.00'),
                'stock': 20,
                'en_oferta': False,
                'descuento': Decimal('0.00'),
                'imagenes': ['eduardo-pastor-3oejsU5OQVk-unsplash.jpg']
            }
        ]
        
        # 5. Crear los productos
        productos_creados = 0
        for producto_info in productos_data:
            vendedor = random.choice(list(vendedores))
            
            # Crear el producto
            producto = Producto.objects.create(
                nombre=producto_info['nombre'],
                descripcion=producto_info['descripcion'],
                stock=producto_info['stock'],
                vendedor=vendedor,
                categoria=producto_info['categoria'],
                color=producto_info['color'],
                en_oferta=producto_info['en_oferta'],
                precio_original=producto_info['precio'],
                descuento=producto_info['descuento']
            )
            
            # Crear las imágenes del producto
            for imagen_nombre in producto_info['imagenes']:
                imagen_path = os.path.join(
                    settings.BASE_DIR, 
                    'tienda_sena', 
                    'static', 
                    'FotosProductos', 
                    imagen_nombre
                )
                
                if os.path.exists(imagen_path):
                    # Crear directorio de destino si no existe
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'productos'), exist_ok=True)
                    
                    # Copiar imagen al directorio media
                    destino_path = os.path.join(settings.MEDIA_ROOT, 'productos', imagen_nombre)
                    shutil.copy2(imagen_path, destino_path)
                    
                    # Crear registro de imagen en la base de datos
                    with open(destino_path, 'rb') as f:
                        imagen_producto = ImagenProducto.objects.create(
                            producto=producto,
                            es_principal=True,  # La primera (y única) imagen será principal
                            orden=1
                        )
                        imagen_producto.imagen.save(imagen_nombre, File(f), save=True)
            
            productos_creados += 1
            self.stdout.write(f'Producto creado: {producto.nombre}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'¡Proceso completado! Se crearon {productos_creados} productos realistas.'
            )
        )
        
        # Mostrar resumen
        self.stdout.write('\n--- RESUMEN ---')
        self.stdout.write(f'Total de productos: {Producto.objects.count()}')
        self.stdout.write(f'Productos en oferta: {Producto.objects.filter(en_oferta=True).count()}')
        self.stdout.write(f'Total de imágenes: {ImagenProducto.objects.count()}')
