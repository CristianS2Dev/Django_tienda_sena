from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre_apellido = models.CharField(max_length=150)
    correo = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    ROLES = (
        (1, "Administrador"),
        (2, "Cliente"),
        (3, "Vendedor"),
    )
    rol = models.IntegerField(choices=ROLES, default=2)
#    imagen_perfil = models.ImageField(upload_to='usuarios/', null=True, blank=True)  # Campo para la foto de perfil

    def __str__(self):
        return f"{self.nombre} - {self.rol}"