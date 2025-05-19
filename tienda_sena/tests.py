from django.test import TestCase
import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from tienda_sena.models import Usuario, Producto, Direccion, Orden, OrdenItem

# Factories
class UsuarioFactory(DjangoModelFactory):
    class Meta:
        model = Usuario

    nombre_apellido = factory.Faker("name")
    documento = factory.Faker("numerify", text="########")
    contacto = factory.Faker("random_int", min=3000000000, max=3999999999)
    correo = factory.Faker("email")
    password = factory.LazyFunction(lambda: "P12345678*")
    rol = 2

class ProductoFactory(DjangoModelFactory):
    class Meta:
        model = Producto

    nombre = factory.Faker("word")
    descripcion = factory.Faker("sentence")
    stock = factory.Faker("random_int", min=1, max=100)
    vendedor = factory.SubFactory(UsuarioFactory)
    categoria = 2
    color = 3
    en_oferta = True
    precio_original = Decimal("100.00")
    descuento = Decimal("10.00")

class DireccionFactory(DjangoModelFactory):
    class Meta:
        model = Direccion

    usuario = factory.SubFactory(UsuarioFactory)
    direccion = factory.Faker("street_address")
    ciudad = factory.Faker("city")
    estado = factory.Faker("state")
    codigo_postal = factory.Faker("postcode")
    pais = "Colombia"
    principal = False

class OrdenFactory(DjangoModelFactory):
    class Meta:
        model = Orden

    usuario = factory.SubFactory(UsuarioFactory)
    direccion = factory.SubFactory(DireccionFactory)
    total = Decimal("150.00")

class OrdenItemFactory(DjangoModelFactory):
    class Meta:
        model = OrdenItem

    orden = factory.SubFactory(OrdenFactory)
    producto = factory.SubFactory(ProductoFactory)
    cantidad = 2
    precio_unitario = Decimal("90.00")

class UsuarioModelTest(TestCase):
    def test_usuario_str(self):
        usuario = UsuarioFactory(nombre_apellido="Juan Perez", rol=2)
        self.assertIn("Juan Perez", str(usuario))