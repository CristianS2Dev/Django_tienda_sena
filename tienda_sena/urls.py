from django.conf.urls.static import static
from django.urls import path
from . import views 
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('registrarse/', views.registrarse, name='registrarse'),

     # Crud productos
    path('lista_productos', views.lista_productos, name='lista_productos'),
    path('agregar_producto', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('producto/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)