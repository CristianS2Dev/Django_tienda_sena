from django.conf.urls.static import static
from django.urls import path
from . import views 
from django.conf import settings


urlpatterns = [
    #URLS de la aplicacion
        path('', views.index, name='index'),
        path('login/', views.login, name='login'),
        path('logout', views.logout, name="logout"),
        path('registrarse/', views.registrarse, name='registrarse'),
        path('modulo_tienda', views.modulo_tienda, name='modulo_tienda'),
        path('sobre_nosotros', views.sobre_nosotros, name='sobre_nosotros'),

    #Perfil Administrador
        path('panel_admin/', views.panel_admin, name='panel_admin'),

        #Crud Usuarios
        path('usuarios', views.usuarios, name='usuarios'),
        path('agregar_usuario', views.agregar_usuario, name="agregar_usuario"),
        path("editar_usuario/<int:id_usuario>/", views.editar_usuario, name="editar_usuario"),
        path("eliminar_usuario/<int:id_usuario>/", views.eliminar_usuario, name="eliminar_usuario"),
        path('perfil_usuario_id/<int:id_usuario>/', views.perfil_usuario_id, name='perfil_usuario_id'),
        path('actualizar_contraseña', views.actualizar_contraseña, name="actualizar_contraseña"),
            #Crud Productos
            path('productos_admnin', views.productos_admnin, name='productos_admnin'),
            path('producto/admin/<int:id_producto>/', views.detalle_producto_admin, name='detalle_producto_admin'),

            path('buscar/', views.buscar_productos, name='buscar_productos'),

            # vistas de carrito
                path('carrito/', views.carrito, name='carrito'),
                path('carrito/agregar/<int:id_producto>/', views.agregar_carrito, name='agregar_carrito'),
                path('carrito/eliminar/<int:id_elemento>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
                path('carrito/actualizar/<int:id_elemento>/', views.actualizar_carrito, name='actualizar_carrito'),
                path('carrito/actualizar/<int:id_elemento>/', views.actualizar_carrito, name='actualizar_carrito'),
                path('pagar_carrito/', views.pagar_carrito, name='pagar_carrito'),
    
    # Vista Usuario
        path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
        path('lista_productos', views.lista_productos, name='lista_productos'),
        path('productos/categoria/<int:id_categoria>/', views.lista_productos, name='productos_por_categoria'),
        path('agregar_producto', views.agregar_producto, name='agregar_producto'),
        path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
        path('producto/user/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
        path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
        path('direccion_usuario', views.direccion_usuario, name='direccion_usuario'),
        path('agregar_direccion', views.agregar_direccion, name='agregar_direccion'),
        path('main_address/<int:id_address>/', views.set_primary_address, name='set_primary_address'),
        path('editar_direccion/<int:id_direccion>/', views.editar_direccion, name='editar_direccion'),
        path('eliminar_direccion/<int:id>/', views.eliminar_direccion, name='eliminar_direccion'),

        # Vendedor
            path('productos/vendedor/<int:id_vendedor>/', views.productos_vendedor, name='productos_vendedor'),
        # Usuario
            path("actualizar_perfil/", views.actualizar_perfil, name="actualizar_perfil"),
            

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)