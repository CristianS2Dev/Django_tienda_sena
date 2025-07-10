from django.contrib import admin
from .models import *

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_apellido', 'correo', 'rol')
    search_fields = ('nombre_apellido', 'correo')
    list_filter = ('rol',)
    ordering = ('-id',)
    list_per_page = 10


@admin.register(SolicitudVendedor)
class SolicitudVendedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'fecha_solicitud')
    search_fields = ('usuario__nombre_apellido',)
    list_filter = ('estado',)
    ordering = ('-fecha_solicitud',)
    list_per_page = 10

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'categoria', 'color', 'en_oferta', 'precio_original', 'descuento', 'vendedor')
    list_filter = ('categoria', 'color', 'vendedor')
    search_fields = ('nombre', 'descripcion')

@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'imagen')
    search_fields = ('producto__nombre',)
    ordering = ('-id',)
    list_per_page = 10

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'creado_en', 'actualizado_en')
    search_fields = ('usuario__nombre_apellido',)
    ordering = ('-id',)

@admin.register(ElementoCarrito)
class ElementoCarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrito', 'producto', 'cantidad')
    search_fields = ('carrito__usuario__nombre_apellido', 'producto__nombre')
    ordering = ('-id',)

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'creado_en', 'total')
    search_fields = ('usuario__nombre_apellido',)
    ordering = ('-id',)

@admin.register(OrdenItem)
class OrdenItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('orden__usuario__nombre_apellido', 'producto__nombre')
    ordering = ('-id',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'mensaje', 'leida', 'fecha')
    search_fields = ('usuario__nombre_apellido', 'mensaje')
    ordering = ('-fecha',)
    list_per_page = 10

