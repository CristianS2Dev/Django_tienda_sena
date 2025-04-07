from django.db import models
from decimal import Decimal

# Create your models here.
class Usuario(models.Model):
    nombre_apellido = models.CharField(max_length=150)
    documento = models.CharField(max_length=20, default="000000")
    contacto = models.IntegerField(default=0)
    correo = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=20)
    ROLES = (
        (1, "Administrador"),
        (2, "Cliente"),
        (3, "Vendedor"),
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    imagen_perfil = models.ImageField(upload_to='usuarios/', null=True, blank=True)  # Campo para la foto de perfil
    direccion = models.CharField(max_length=254, default="none")
    
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


