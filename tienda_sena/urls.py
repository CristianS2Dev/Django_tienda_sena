from django.conf.urls.static import static
from django.urls import path
from . import views 
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),

    #Perfil Administrador
    path('panel_admin/', views.panel_admin, name='panel_admin'),

       #Crud Usuarios
    path('usuarios', views.usuarios, name='usuarios'),
    path('agregar_usuario', views.agregar_usuario, name="agregar_usuario"),
    path("editar_usuario/<int:id_usuario>/", views.editar_usuario, name="editar_usuario"),
    path("eliminar_usuario/<int:id_usuario>/", views.eliminar_usuario, name="eliminar_usuario"),
        #Crud Productos
    path('productos', views.productos, name='productos'),

    
    # Crud productos Vista Usuario
    path('lista_productos', views.lista_productos, name='lista_productos'),
    path('agregar_producto', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('producto/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
     path('productos/categoria/<int:categoria>/', views.productos_por_categoria, name='productos_por_categoria'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)