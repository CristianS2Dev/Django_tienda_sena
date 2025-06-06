from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from tienda_sena.models import Usuario

class IniciarSesionTest(TestCase):
    def test_sesion_correcta_usuario_rol_2(self):
        response = self.client.post(reverse("login"), {
            "correo": "ronaldoo@gmail.com",
            "password": "Ronaldo1234*"
        })
        self.assertRedirects(response, reverse("index"))  # Ajusta si tu vista redirige a index

    def test_sesion_correcta_usuario_rol_1(self):
        response = self.client.post(reverse("login"), {
            "correo": "georgina@hotmail.com",
            "password": "Georgina1234*"
        })
        self.assertRedirects(response, reverse("index"))  # Ajusta si tu vista redirige a index

    def test_usuario_no_existe(self):
        response = self.client.post(reverse("login"), {
            "correo": "noexiste@example.com",
            "password": "algo"
        })
        self.assertRedirects(response, reverse("login"))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Usuario o contraseña incorrectos...", [m.message for m in messages])

    def test_contraseña_incorrecta(self):
        response = self.client.post(reverse("login"), {
            "correo": "ronaldoo@gmail.com",
            "password": "incorrecta"
        })
        self.assertRedirects(response, reverse("login"))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Usuario o contraseña incorrectos...", [m.message for m in messages])

    def test_get_con_sesion(self):
        session = self.client.session
        session["usuario_id"] = self.usuario_normal.id
        session.save()
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)  # O ajusta según el comportamiento real

    def test_get_sin_sesion(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")