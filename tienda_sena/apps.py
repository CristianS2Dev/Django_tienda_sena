from django.apps import AppConfig


class TiendaSenaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tienda_sena'
    
    def ready(self):
        import tienda_sena.signals
