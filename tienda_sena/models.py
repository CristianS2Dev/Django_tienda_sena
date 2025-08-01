from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from django.utils import timezone
from cloudinary.models import CloudinaryField
from cloudinary.models import CloudinaryField


# Create your models here.

class Usuario(models.Model):
    """
    Modelo para los usuarios de la tienda.

    :model:`tienda_sena.Usuario`

    Campos:
        nombre_apellido (CharField): Nombre completo del usuario.
        documento (CharField): Documento de identidad.
        contacto (IntegerField): Número de contacto.
        correo (CharField): Correo electrónico único.
        password (CharField): Contraseña encriptada.
        rol (IntegerField): Rol del usuario (Administrador, Cliente, Vendedor).
        imagen_perfil (ImageField): Imagen de perfil del usuario.
        activo (BooleanField): Indica si el usuario está activo o deshabilitado.
    """
    nombre_apellido = models.CharField(max_length=150)
    documento = models.CharField(max_length=20, default="000000")
    contacto = models.IntegerField(default=0)
    correo = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    ROLES = (
        (1, "Administrador"),
        (2, "Cliente"),
        (3, "Vendedor"),
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    activo = models.BooleanField(default=True, help_text="Indica si el usuario está activo")
    correo_verificado = models.BooleanField(default=False, help_text="Indica si el correo electrónico ha sido verificado")
    imagen_perfil = models.ImageField(upload_to='usuarios/perfiles/', null=True, blank=True, help_text="Imagen de perfil optimizada")
    imagen_perfil_original = models.ImageField(upload_to='usuarios/originales/', null=True, blank=True, help_text="Imagen de perfil original")
    codigo_verificacion = models.IntegerField(null=True, blank=True)
    fecha_codigo_verificacion = models.DateTimeField(null=True, blank=True, help_text="Fecha cuando se generó el código de verificación")
    tipo_codigo = models.CharField(max_length=20, null=True, blank=True, help_text="Tipo de código: 'registro' o 'password'", default='registro')
    
    def save(self, *args, **kwargs):
        """Sobrescribe el método save para encriptar la contraseña antes de guardar."""
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_apellido} - {self.rol}"
    

class SolicitudVendedor(models.Model):
    """
    Modelo para las solicitudes de los vendedores.

    :model:`tienda_sena.SolicitudVendedor`

    Campos:
        usuario (ForeignKey): Usuario que solicita ser vendedor.
        certificado (ImageField): Certificado adjunto.
        estado (CharField): Estado de la solicitud (pendiente, aprobado, rechazado).
        fecha_solicitud (DateTimeField): Fecha de la solicitud.
        observacion (TextField): Observaciones adicionales.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    certificado = models.ImageField(upload_to='certificado/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)


class Direccion(models.Model):
    """
    Modelo para las direcciones de los usuarios.

    :model:`tienda_sena.Direccion`

    Campos:
        usuario (ForeignKey): Usuario propietario de la dirección.
        direccion (CharField): Dirección física.
        ciudad (CharField): Ciudad.
        estado (CharField): Estado o departamento.
        codigo_postal (CharField): Código postal.
        pais (CharField): País.
        principal (BooleanField): Si es la dirección principal del usuario.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100, default="Colombia")
    principal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para asegurarse de que solo haya una dirección principal por usuario."""
        if self.principal:
            Direccion.objects.filter(usuario=self.usuario, principal=True).exclude(id=self.id).update(principal=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}, {self.estado}, {self.pais}"
    


class Producto(models.Model):
    """
    Modelo para los productos.

    :model:`tienda_sena.Producto`

    Campos:
        nombre (CharField): Nombre del producto.
        descripcion (CharField): Descripción breve.
        stock (IntegerField): Cantidad disponible.
        vendedor (ForeignKey): Usuario vendedor.
        categoria (IntegerField): Categoría del producto.
        color (IntegerField): Color principal.
        en_oferta (BooleanField): Si el producto está en oferta.
        precio_original (DecimalField): Precio original.
        descuento (DecimalField): Porcentaje de descuento.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=254)
    stock = models.IntegerField()
    vendedor = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    
    CATEGORIAS = (
        (0, 'Ninguna'),
        (1, 'Electrónicos'),
        (2, 'Ropa'),
        (3, 'Hogar'),
        (4, 'Deportes'),
        (5, 'Libros'),
        (6, 'Juguetes'),
        (7, 'Automotriz'),
        (8, 'Salud y Belleza'),
        (9, 'Jardín'),
        (10, 'Herramientas'),
    )
    categoria = models.IntegerField(choices=CATEGORIAS, default=0)
    COLORES = (
        (0,"Ninguno"),
        (1,"Gris"),
        (2,"Blanco"),
        (3,"Negro"),
        (4,"Amarillo"),
        (5,"Azul"),
        (6,"Rojo"),
    )  
    color = models.IntegerField(choices=COLORES, default=0, null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    activo = models.BooleanField(default=True, help_text="Indica si el producto está activo o deshabilitado")
    def clean(self):
        """
        Validaciones personalizadas para el modelo Producto.

        - El stock no puede ser negativo.
        - El precio original no puede ser negativo.
        - El descuento debe estar entre 0 y 100.
        - El precio final no puede ser negativo.
        """
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        if self.precio_original is not None and self.precio_original < 0:
            raise ValidationError("El precio original no puede ser negativo.")
        if self.descuento < 0:
            raise ValidationError("El descuento no puede ser negativo.")
        if self.descuento > 100:
            raise ValidationError("El descuento no puede ser mayor al 100%.")
        if self.en_oferta and self.precio_original is not None:
            precio_final = self.precio_original - (self.precio_original * self.descuento / Decimal(100))
            if precio_final < 0:
                raise ValidationError("El precio con descuento no puede ser negativo.")

    @property
    def precio(self):
        """
        Calcula el precio final basado en el descuento.

        Returns:
            Decimal: Precio final del producto.
        """
        if self.en_oferta and self.descuento > 0:
            return round(self.precio_original - (self.precio_original * self.descuento / Decimal(100)), 2)
        return self.precio_original

    @property
    def imagen_principal(self):
        """
        Obtiene la imagen principal del producto de manera segura.
        
        Returns:
            ImagenProducto or None: La imagen principal o None si no existe
        """
        return self.imagenes.filter(es_principal=True).first() or self.imagenes.first()
    
    def get_imagen_principal_url(self, transformacion=None):
        """
        Obtiene la URL de la imagen principal de manera segura.
        
        Args:
            transformacion (dict): Transformaciones para Cloudinary
            
        Returns:
            str: URL de la imagen o URL por defecto
        """
        imagen = self.imagen_principal
        if imagen:
            url = imagen.get_imagen_url(transformacion)
            if url:
                return url
        
        # URL por defecto si no hay imagen
        from django.templatetags.static import static
        return static('assets/product.png')

    def __str__(self):
        return f"{self.nombre} - ({self.stock} unidades)"
    

class ImagenProducto(models.Model):
    """
    Modelo para las imágenes de los productos con integración de Cloudinary.

    :model:`tienda_sena.ImagenProducto`

    Campos:
        producto (ForeignKey): Producto al que pertenece la imagen.
        imagen_cloudinary (CloudinaryField): Imagen almacenada en Cloudinary.
        cloudinary_public_id (CharField): ID público en Cloudinary.
        cloudinary_version (CharField): Versión de la imagen en Cloudinary.
        imagen (ImageField): Imagen local (backup/compatibilidad).
        imagen_original (ImageField): Imagen original sin procesar (backup).
        miniatura (ImageField): Miniatura local (backup).
        es_principal (BooleanField): Si es la imagen principal del producto.
        orden (IntegerField): Orden de visualización de la imagen.
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    
    # Campos de Cloudinary
    imagen_cloudinary = CloudinaryField('image', null=True, blank=True, help_text="Imagen almacenada en Cloudinary")
    cloudinary_public_id = models.CharField(max_length=255, null=True, blank=True, help_text="ID público en Cloudinary")
    cloudinary_version = models.CharField(max_length=50, null=True, blank=True, help_text="Versión en Cloudinary")
    
    # Campos locales (para compatibilidad/backup)
    imagen = models.ImageField(upload_to='productos/optimizadas/', null=True, blank=True, help_text="Imagen optimizada local")
    imagen_original = models.ImageField(upload_to='productos/originales/', null=True, blank=True, help_text="Imagen original local")
    miniatura = models.ImageField(upload_to='productos/miniaturas/', null=True, blank=True, help_text="Miniatura local")
    
    # Campos de control
    es_principal = models.BooleanField(default=False, help_text="Imagen principal del producto")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    usa_cloudinary = models.BooleanField(default=True, help_text="Si usa Cloudinary o almacenamiento local")
    
    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'
    
    def save(self, *args, **kwargs):
        # Si es la primera imagen del producto, hacerla principal
        if not self.producto.imagenes.exists():
            self.es_principal = True
        
        # Si se marca como principal, desmarcar las demás
        if self.es_principal:
            ImagenProducto.objects.filter(
                producto=self.producto, 
                es_principal=True
            ).exclude(id=self.id).update(es_principal=False)
        
        super().save(*args, **kwargs)
    
    def get_imagen_url(self, transformacion=None):
        """
        Obtiene la URL de la imagen, priorizando Cloudinary.
        
        Args:
            transformacion (dict): Transformaciones específicas para Cloudinary
        
        Returns:
            str: URL de la imagen
        """
        if self.usa_cloudinary and self.cloudinary_public_id:
            if transformacion:
                from cloudinary import CloudinaryImage
                return CloudinaryImage(self.cloudinary_public_id).build_url(**transformacion)
            return self.imagen_cloudinary.url if self.imagen_cloudinary else None
        
        # Fallback a imagen local solo si existe
        if self.imagen and hasattr(self.imagen, 'url'):
            try:
                return self.imagen.url
            except ValueError:
                # El archivo no existe físicamente
                return None
        
        return None
    
    def get_thumbnail_url(self):
        """Obtiene URL de la miniatura optimizada."""
        return self.get_imagen_url({
            'width': 300, 
            'height': 300, 
            'crop': 'fill',
            'quality': 'auto',
            'fetch_format': 'auto'
        })
    
    def get_banner_url(self):
        """Obtiene URL para banner (listado de productos)."""
        return self.get_imagen_url({
            'width': 1200, 
            'height': 400, 
            'crop': 'fill',
            'quality': 'auto',
            'fetch_format': 'auto'
        })
    
    def get_zoom_url(self):
        """Obtiene URL para zoom (detalle de producto)."""
        return self.get_imagen_url({
            'width': 1500, 
            'height': 1500, 
            'crop': 'limit',
            'quality': 'auto',
            'fetch_format': 'auto'
        })
    
    def get_optimizada_url(self):
        """Obtiene URL de la imagen optimizada estándar."""
        return self.get_imagen_url({
            'width': 800, 
            'height': 800, 
            'crop': 'limit',
            'quality': 'auto',
            'fetch_format': 'auto'
        })
    
    def eliminar_de_cloudinary(self):
        """
        Elimina la imagen de Cloudinary.
        
        Returns:
            bool: True si se eliminó correctamente
        """
        if self.cloudinary_public_id:
            try:
                from .cloudinary_utils import cloudinary_manager
                return cloudinary_manager.eliminar_imagen(self.cloudinary_public_id)
            except Exception:
                return False
        return False
    
    def migrar_a_cloudinary(self):
        """
        Migra una imagen local a Cloudinary.
        
        Returns:
            bool: True si la migración fue exitosa
        """
        if self.imagen and not self.cloudinary_public_id:
            try:
                from .cloudinary_utils import cloudinary_manager
                resultado = cloudinary_manager.subir_imagen_producto(
                    self.imagen, 
                    self.producto.id, 
                    self.es_principal
                )
                
                if resultado['success']:
                    self.cloudinary_public_id = resultado['public_id']
                    self.cloudinary_version = str(resultado['version'])
                    self.usa_cloudinary = True
                    self.save()
                    return True
            except Exception:
                pass
        return False
    
    def delete(self, *args, **kwargs):
        """Sobrescribe delete para eliminar también de Cloudinary."""
        # Eliminar de Cloudinary si existe
        if self.cloudinary_public_id:
            self.eliminar_de_cloudinary()
        
        # Llamar al delete original
        super().delete(*args, **kwargs)

    def __str__(self):
        tipo = "Cloudinary" if self.usa_cloudinary else "Local"
        return f"Imagen {tipo} de {self.producto.nombre} {'(Principal)' if self.es_principal else ''}"


class Carrito(models.Model):
    """
    Modelo para el carrito de compras.

    :model:`tienda_sena.Carrito`

    Campos:
        usuario (ForeignKey): Usuario propietario del carrito.
        creado_en (DateTimeField): Fecha de creación.
        actualizado_en (DateTimeField): Fecha de última actualización.
    """
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True, related_name='carritos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def total(self):
        """
        Calcula el total del carrito sumando los subtotales de los elementos.

        Returns:
            Decimal: Total del carrito.
        """
        return sum(item.subtotal() for item in self.elementos.all())

    def __str__(self):
        return f"Carrito de {self.usuario.nombre_apellido if self.usuario else 'Invitado'}"


class ElementoCarrito(models.Model):
    """
    Modelo para los elementos del carrito.

    :model:`tienda_sena.ElementoCarrito`

    Campos:
        carrito (ForeignKey): Carrito al que pertenece el elemento.
        producto (ForeignKey): Producto seleccionado.
        cantidad (PositiveIntegerField): Cantidad del producto.
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """
        Calcula el subtotal del elemento (precio del producto * cantidad).

        Returns:
            Decimal: Subtotal del elemento.
        """
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"
    

class Orden(models.Model):
    """
    Modelo para las órdenes de compra.

    :model:`tienda_sena.Orden`

    Campos:
        usuario (ForeignKey): Usuario que realiza la orden.
        direccion (ForeignKey): Dirección de envío.
        creado_en (DateTimeField): Fecha de creación.
        total (DecimalField): Total de la orden.
        estado_pago (CharField): Estado del pago (pendiente, pagado, rechazado).
        subtotal (DecimalField): Subtotal sin envío.
        costo_envio (DecimalField): Costo del envío.
        metodo_envio (CharField): Método de envío seleccionado.
        notas (TextField): Notas adicionales del cliente.
    """
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Nuevos campos para checkout mejorado
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    METODOS_ENVIO = (
        ('estandar', 'Envío Estándar (3-5 días)'),
        ('express', 'Envío Express (1-2 días)'),
        ('recoger', 'Recoger en Tienda'),
    )
    metodo_envio = models.CharField(max_length=20, choices=METODOS_ENVIO, default='estandar')
    notas = models.TextField(blank=True, null=True, help_text="Notas adicionales del cliente")
    
    ESTADO_PAGO = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('pagado', 'Pagado'),
        ('rechazado', 'Rechazado'),
    )
    estado_pago = models.CharField(max_length=10, choices=ESTADO_PAGO, default='aprobado')
    
    def calcular_total(self):
        """Calcula el total como subtotal + costo de envío"""
        return self.subtotal + self.costo_envio
    
    def save(self, *args, **kwargs):
        # Calcular total automáticamente
        if self.subtotal and self.costo_envio is not None:
            self.total = self.calcular_total()
        super().save(*args, **kwargs)


class OrdenItem(models.Model):
    """
    Modelo para los elementos de una orden.

    :model:`tienda_sena.OrdenItem`

    Campos:
        orden (ForeignKey): Orden a la que pertenece el elemento.
        producto (ForeignKey): Producto comprado.
        cantidad (PositiveIntegerField): Cantidad comprada.
        precio_unitario (DecimalField): Precio unitario del producto.
    """
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)


class Notificacion(models.Model):
    """
    Modelo para las notificaciones de los usuarios.

    :model:`tienda_sena.Notificacion`

    Campos:
        usuario (ForeignKey): Usuario destinatario.
        titulo (CharField): Título de la notificación.
        mensaje (CharField): Mensaje de la notificación.
        tipo (CharField): Tipo de notificación para diferentes estilos.
        url (CharField): URL opcional para redirección.
        leida (BooleanField): Si la notificación ha sido leída.
        fecha (DateTimeField): Fecha de creación.
        fecha_leida (DateTimeField): Fecha cuando fue leída.
    """
    TIPOS_NOTIFICACION = [
        ('info', 'Información'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('pedido', 'Pedido'),
        ('vendedor', 'Vendedor'),
        ('sistema', 'Sistema'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, default="Notificación")
    mensaje = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPOS_NOTIFICACION, default='info')
    url = models.CharField(max_length=200, blank=True, null=True)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.nombre_apellido}"
    
    def marcar_como_leida(self):
        """Marca la notificación como leída"""
        if not self.leida:
            self.leida = True
            self.fecha_leida = timezone.now()
            self.save()
    
    def get_icono(self):
        """Retorna el icono FontAwesome según el tipo"""
        iconos = {
            'info': 'fas fa-info-circle text-primary',
            'success': 'fas fa-check-circle text-success',
            'warning': 'fas fa-exclamation-triangle text-warning',
            'error': 'fas fa-times-circle text-danger',
            'pedido': 'fas fa-shopping-cart text-info',
            'vendedor': 'fas fa-store text-warning',
            'sistema': 'fas fa-cog text-secondary',
        }
        return iconos.get(self.tipo, 'fas fa-bell text-primary')


class CalificacionProducto(models.Model):
    """
    Modelo para guardar calificaciones y comentarios de productos comprados por usuarios.

    Campos:
        usuario (ForeignKey): Usuario que califica.
        producto (ForeignKey): Producto calificado.
        orden_item (ForeignKey): Relación con el ítem de la orden (opcional, para validar compra).
        calificacion (IntegerField): Valor de la calificación (1 a 5).
        comentario (TextField): Comentario del usuario.
        fecha (DateTimeField): Fecha de la calificación.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    orden_item = models.ForeignKey('OrdenItem', on_delete=models.CASCADE, null=True, blank=True)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto', 'orden_item')  # Un usuario solo puede calificar una vez por compra

    def __str__(self):
        return f"{self.usuario.nombre_apellido} - {self.producto.nombre} ({self.calificacion} estrellas)"