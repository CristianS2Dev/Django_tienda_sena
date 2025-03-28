from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import *
from .utils import *

from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        try:
            q = Usuario.objects.get(correo = correo, password = password)
            # Autenticación: Creamos la variable de sesión +++++++++
            request.session["pista"] = {
                "id": q.id,
                "rol": q.rol,
                "nombre": q.nombre_apellido
            }
            messages.success(request, "Bienvenido!!")
            return redirect("principal")
        except Usuario.DoesNotExist:
            # Autenticación: Vaciamos la variable de sesión ----------
            request.session["pista"] = None

            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect("login")
    else:
        # capturamos la variable de sesión
        verificar = request.session.get("pista", False)
        if verificar:
            return redirect("index")
        else:
            return render(request, "login.html")

def logout(request):
    try:
        del request.session["pista"]
        return redirect("index")
    except:
        messages.error(request, "Ocurrio un error")
        return redirect("index")

def registrarse(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol = request.POST.get("rol")
        imagen_perfil = request.FILES.get("imagen_perfil")  # para obtener la imagen del formulario
        try:
            if imagen_perfil:
            # Validar formatos permitidos
                formatos_permitidos = ["image/jpeg", "image/png", "image/webp"]
                if imagen_perfil.content_type not in formatos_permitidos:
                    raise ValidationError(f"Formato no permitido: {imagen_perfil.content_type}. Solo se aceptan JPEG, PNG o WEBP.")
            usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                password=password,
                rol=rol,
                imagen_perfil=imagen_perfil if imagen_perfil else None  # Si es 1 solo archivo
            )
            usuario.save()
            messages.success(request, "Usuario registrado correctamente!")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("registrarse")
    else:
        return render(request, "registrarse.html")


