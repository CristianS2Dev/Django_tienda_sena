from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

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
    imagen_perfil = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    
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
        (0, ""),
        (1, "Moda"),
        (2, "Tecnologia"),
        (3, "Artesania"),
        (4, "Accesorios"),
        (5, "Servicios"),
        (6, "Otros"),
    )
    categoria = models.IntegerField(choices=CATEGORIAS, default=0, null=True, blank=True)
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

    def __str__(self):
        return f"{self.nombre} - ({self.stock} unidades)"
    

class ImagenProducto(models.Model):
    """
    Modelo para las imágenes de los productos.

    :model:`tienda_sena.ImagenProducto`

    Campos:
        producto (ForeignKey): Producto al que pertenece la imagen.
        imagen (ImageField): Archivo de imagen.
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


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
    """
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ESTADO_PAGO = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('rechazado', 'Rechazado'),
    )
    estado_pago = models.CharField(max_length=10, choices=ESTADO_PAGO, default='pendiente')


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
        mensaje (CharField): Mensaje de la notificación.
        leida (BooleanField): Si la notificación ha sido leída.
        fecha (DateTimeField): Fecha de creación.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)


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