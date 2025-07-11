from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_sena', '0021_add_categoria_system'),
    ]

    operations = [
        # Primero eliminar la referencia ForeignKey
        migrations.RemoveField(
            model_name='producto',
            name='categoria',
        ),
        
        # Agregar de vuelta el campo IntegerField original
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.IntegerField(choices=[
                (0, 'Ninguna'),
                (1, 'Electrónicos'),
                (2, 'Ropa'),
                (3, 'Hogar'),
                (4, 'Deportes'),
                (5, 'Libros'),
                (6, 'Juguetes'),
                (7, 'Automotriz'),
                (8, 'Salud y Belleza'),
                (9, 'Jardín'),
                (10, 'Herramientas'),
            ], default=0),
        ),
        
        # Eliminar completamente el modelo Categoria
        migrations.DeleteModel(
            name='Categoria',
        ),
    ]
