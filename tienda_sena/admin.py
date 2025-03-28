from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_apellido', 'correo', 'rol')
    search_fields = ('nombre_apellido', 'correo')
    list_filter = ('rol',)
    ordering = ('-id',)
    list_per_page = 10

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio', 'stock', 'categoria')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria',)
    ordering = ('-id',)
    list_per_page = 10

@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'imagen')
    search_fields = ('producto__nombre',)
    ordering = ('-id',)
    list_per_page = 10