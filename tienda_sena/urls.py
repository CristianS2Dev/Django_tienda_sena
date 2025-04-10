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

    #Perfil Administrador
        path('panel_admin/', views.panel_admin, name='panel_admin'),

        #Crud Usuarios
        path('usuarios', views.usuarios, name='usuarios'),
        path('agregar_usuario', views.agregar_usuario, name="agregar_usuario"),
        path("editar_usuario/<int:id_usuario>/", views.editar_usuario, name="editar_usuario"),
        path("eliminar_usuario/<int:id_usuario>/", views.eliminar_usuario, name="eliminar_usuario"),
        path('perfil_usuario_id/<int:id_usuario>/', views.perfil_usuario_id, name='perfil_usuario_id'),
        
            #Crud Productos
            path('productos_admnin', views.productos_admnin, name='productos_admnin'),
            path('producto/admin/<int:id_producto>/', views.detalle_producto_admin, name='detalle_producto_admin'),

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
        path('agregar_producto', views.agregar_producto, name='agregar_producto'),
        path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
        path('producto/user/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
        path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
        path('productos/categoria/<int:categoria>/', views.productos_por_categoria, name='productos_por_categoria'),
        # Vendedor
            path('productos/vendedor/<int:id_vendedor>/', views.productos_vendedor, name='productos_vendedor'),
        # Usuario
            
            

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)