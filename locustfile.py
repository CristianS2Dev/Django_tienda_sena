from locust import HttpUser, TaskSet, task, between

class ClienteBehavior(TaskSet):
    def on_start(self):
        """Ejecutar al inicio de cada usuario simulado (cliente)."""
        self.login()

    def login(self):
        """Simula el inicio de sesión como cliente."""
        response = self.client.get("/login/")
        csrf_token = response.cookies.get("csrftoken")

        if not csrf_token:
            print("No se pudo obtener el token CSRF para el inicio de sesión del cliente.")
            return

        response = self.client.post(
            "/login/",
            {
                "correo": "maria@gmail.com",  # Usuario cliente
                "password": "ClientePassword123*"
            },
            headers={"X-CSRFToken": csrf_token}
        )

        if response.status_code == 200:
            print("Inicio de sesión exitoso como cliente.")
        else:
            print(f"Error al iniciar sesión como cliente: {response.status_code} - {response.text}")

    @task(1)
    def enviar_solicitud_vendedor(self):
        """Simula el envío de una solicitud para ser vendedor."""
        response = self.client.get("/solicitudes_vendedor/")
        csrf_token = response.cookies.get("csrftoken")

        if not csrf_token:
            print("No se pudo obtener el token CSRF para enviar la solicitud.")
            return

        response = self.client.post(
            "/solicitudes_vendedor/enviar/",
            headers={"X-CSRFToken": csrf_token}
        )

        if response.status_code == 200:
            print("Solicitud para ser vendedor enviada exitosamente.")
        else:
            print(f"Error al enviar la solicitud: {response.status_code} - {response.text}")


class AdminBehavior(TaskSet):
    def on_start(self):
        """Ejecutar al inicio de cada usuario simulado (administrador)."""
        self.login()

    def login(self):
        """Simula el inicio de sesión como administrador."""
        response = self.client.get("/login/")
        csrf_token = response.cookies.get("csrftoken")

        if not csrf_token:
            print("No se pudo obtener el token CSRF para el inicio de sesión del administrador.")
            return

        response = self.client.post(
            "/login/",
            {
                "correo": "tiendaSena@gmail.com",  # Usuario administrador
                "password": "AdminPassword123*"
            },
            headers={"X-CSRFToken": csrf_token}
        )

        if response.status_code == 200:
            print("Inicio de sesión exitoso como administrador.")
        else:
            print(f"Error al iniciar sesión como administrador: {response.status_code} - {response.text}")

    @task(1)
    def aprobar_solicitud(self):
        """Simula la aprobación de una solicitud de vendedor."""
        response = self.client.get("/administrador/solicitudes_vendedor/")
        csrf_token = response.cookies.get("csrftoken")

        if not csrf_token:
            print("No se pudo obtener el token CSRF para aprobar la solicitud.")
            return

        response = self.client.post(
            "/administrador/solicitudes_vendedor/aprobar/1/",
            headers={"X-CSRFToken": csrf_token}
        )

        if response.status_code == 200:
            print("Solicitud aprobada exitosamente.")
        else:
            print(f"Error al aprobar la solicitud: {response.status_code} - {response.text}")

    @task(1)
    def rechazar_solicitud(self):
        """Simula el rechazo de una solicitud de vendedor."""
        response = self.client.get("/administrador/solicitudes_vendedor/")
        csrf_token = response.cookies.get("csrftoken")

        if not csrf_token:
            print("No se pudo obtener el token CSRF para rechazar la solicitud.")
            return

        response = self.client.post(
            "/administrador/solicitudes_vendedor/rechazar/1/",
            headers={"X-CSRFToken": csrf_token}
        )

        if response.status_code == 200:
            print("Solicitud rechazada exitosamente.")
        else:
            print(f"Error al rechazar la solicitud: {response.status_code} - {response.text}")


class ClienteUser(HttpUser):
    tasks = [ClienteBehavior]
    wait_time = between(1, 5)  
    host = "http://127.0.0.1:8000"


class AdminUser(HttpUser):
    tasks = [AdminBehavior]
    wait_time = between(1, 5)  # Tiempo de espera entre tareas (1-5 segundos)
    host = "http://127.0.0.1:8000" 