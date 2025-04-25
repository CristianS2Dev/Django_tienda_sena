from django.core.management.base import BaseCommand
from tienda_sena.models import Carrito
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Elimina carritos huérfanos (sin usuario) y viejos'

    def handle(self, *args, **kwargs):
        dias = 7  # Cambia esto si quieres otro periodo
        limite = timezone.now() - timedelta(days=dias)
        carritos = Carrito.objects.filter(usuario__isnull=True, actualizado_en__lt=limite)
        total = carritos.count()
        carritos.delete()
        self.stdout.write(self.style.SUCCESS(f'Se eliminaron {total} carritos huérfanos de más de {dias} días.'))