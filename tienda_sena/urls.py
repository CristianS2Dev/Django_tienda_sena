from django.conf.urls.static import static
from django.urls import path
from . import views 
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('registrarse/', views.registrarse, name='registrarse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)