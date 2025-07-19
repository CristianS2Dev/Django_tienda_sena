from django.core.management.base import BaseCommand
from tienda_sena.models import Notificacion

class Command(BaseCommand):
    help = 'Actualiza las notificaciones existentes con los nuevos campos'

    def handle(self, *args, **options):
        # Actualizar notificaciones existentes que no tienen título
        notificaciones_sin_titulo = Notificacion.objects.filter(titulo="Notificación")
        count = 0
        
        for notificacion in notificaciones_sin_titulo:
            # Asignar títulos y tipos basados en el contenido del mensaje
            mensaje = notificacion.mensaje.lower()
            
            if "aprobada" in mensaje or "aprobado" in mensaje:
                notificacion.titulo = "¡Solicitud Aprobada!"
                notificacion.tipo = "success"
            elif "rechaza" in mensaje or "rechazado" in mensaje:
                notificacion.titulo = "Solicitud Rechazada"
                notificacion.tipo = "warning"
            elif "bienvenido" in mensaje:
                notificacion.titulo = "¡Bienvenido!"
                notificacion.tipo = "success"
            elif "pedido" in mensaje:
                notificacion.titulo = "Actualización de Pedido"
                notificacion.tipo = "info"
            elif "producto" in mensaje:
                notificacion.titulo = "Notificación de Producto"
                notificacion.tipo = "info"
            else:
                notificacion.titulo = "Notificación del Sistema"
                notificacion.tipo = "info"
            
            notificacion.save()
            count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {count} notifications'
            )
        )
