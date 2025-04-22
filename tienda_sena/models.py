from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

# Create your models here.
class Usuario(models.Model):
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
    imagen_perfil = models.ImageField(upload_to='usuarios/', null=True, blank=True)  # Campo para la foto de perfil
    direccion = models.CharField(max_length=254, default="none")
    certificado = models.ImageField(upload_to='certificado/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Encriptar la contraseña si no está encriptada
        if not self.password.startswith('pbkdf2_'):  # Evitar encriptar una contraseña ya encriptada
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.nombre_apellido} - {self.rol}"
    
class Producto(models.Model):
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
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        if self.precio_original is not None and self.precio_original < 0:
            raise ValidationError("El precio original no puede ser negativo.")
        if self.descuento < 0:
            raise ValidationError("El descuento no puede ser negativo.")

    @property
    def precio(self):
        """Calcula el precio final basado en el descuento."""
        if self.en_oferta and self.descuento > 0:
            return round(self.precio_original - (self.precio_original * self.descuento / Decimal(100)), 2)
        return self.precio_original

    def __str__(self):
        return f"{self.nombre} - ({self.stock} unidades)"
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


class Carrito(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True, related_name='carritos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def total(self):
        """Calcula el total del carrito sumando los subtotales de los elementos."""
        return sum(item.subtotal() for item in self.elementos.all()) # suma de los subtotales de cada elemento

    def __str__(self):
        return f"Carrito de {self.usuario.nombre if self.usuario else 'Invitado'}"

class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='elementos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """Calcula el subtotal del elemento (precio del producto * cantidad)."""
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"
    

class Orden(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Puedes agregar más campos según lo necesites

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)