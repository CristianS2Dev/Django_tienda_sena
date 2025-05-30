from django.test import TestCase, Client
from tienda_sena.models import Usuario

class UsuariosJsonTest(TestCase):
    def setUp(self):
        self.client = Client()
        Usuario.objects.create(nombre_apellido="Juanito", correo="juanito@gmail.com", password="1234", rol=2)

    def test_usuarios_json(self):
        response = self.client.get('/usuarios/json/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)