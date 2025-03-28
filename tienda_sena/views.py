from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from decimal import Decimal
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


# -----------------------------------------------------  
        #CRUD Listar productos usuario
# -----------------------------------------------------

def lista_productos(request):
    q = Producto.objects.all()
    contexto = {'data': q}
    return (render(request, 'productos/listar_productos.html', contexto))

# -----------------------------------------------------
@session_rol_permission(1, 3)
def agregar_producto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        # Manejar valores predeterminados para precio_original y descuento
        precio_original = request.POST.get("precio_original", "0")
        descuento = request.POST.get("descuento", "0")
        try:
            precio_original = Decimal(precio_original) if precio_original else Decimal(0)
            descuento = Decimal(descuento) if descuento else Decimal(0)
            en_oferta = request.POST.get("en_oferta") == "on"
            stock = request.POST.get("stock")
            vendedor = request.POST.get("vendedor")
            categoria = request.POST.get("categoria")
            color = request.POST.get("color")
            imagenes = request.FILES.getlist("imagenes")
            # Validar imágenes
            if len(imagenes) > 5:
                raise ValidationError("No puedes subir más de 5 imágenes.")
            formatos_permitidos = ["image/jpeg", "image/png", "image/gif", "image/webp"]
            for imagen in imagenes:
                if imagen.content_type not in formatos_permitidos:
                    raise ValidationError(f"Formato no permitido: {imagen.content_type}. Solo se aceptan JPEG, PNG, GIF o WEBP.")
            # Crear el producto
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio_original=precio_original,
                descuento=descuento,
                en_oferta=en_oferta,
                stock=stock,
                vendedor_id=vendedor,
                categoria=categoria,
                color=color,
            )
            producto.save()
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)
            messages.success(request, "Producto guardado correctamente!")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("lista_productos")
    else:
        user = request.session.get("pista")
        roles = dict(Usuario.ROLES).get(user["rol"], "Desconocido")
        return render(request, "productos/agregar_productos.html", {'user': user, 'roles': roles})
    
# -----------------------------------------------------
@session_rol_permission(1, 3)
def editar_producto(request, id_producto):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        precio_original = request.POST.get("precio_original")
        descuento = Decimal(request.POST.get("descuento", 0))  # Porcentaje de descuento
        en_oferta = request.POST.get("en_oferta") == "on"
        stock = request.POST.get("stock")
        vendedor = request.POST.get("vendedor")
        categoria = request.POST.get("categoria")
        color = request.POST.get("color")
        imagenes = request.FILES.getlist("imagenes")  # Obtener las imágenes subidas
        try:
            # Obtener el producto a editar
            q = Producto.objects.get(pk=id_producto)

            # Actualizar los campos del producto
            q.nombre = nombre
            q.descripcion = descripcion

            # Convertir los valores a Decimal para evitar problemas en el cálculo
            precio = Decimal(precio)
            q.precio_original = precio
            descuento_decimal = Decimal(descuento) if descuento else Decimal(0)
            q.descuento = descuento_decimal
            q.en_oferta = en_oferta

            # Calcular el precio final si está en oferta
            if en_oferta and descuento_decimal > 0:
                q.precio = round(precio - (precio * descuento_decimal / Decimal(100)), 2)
            else:
                q.precio = precio

            q.stock = stock
            q.vendedor_id = vendedor
            q.categoria = categoria
            q.color = color
            q.save()

            # Guardar las nuevas imágenes asociadas al producto
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=q, imagen=imagen)

            messages.success(request, "Producto actualizado correctamente!")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("lista_productos")
    else:
        # Obtener el producto para mostrarlo en el formulario de edición
        q = Producto.objects.get(pk=id_producto)
        return render(request, "productos/agregar_productos.html", {"dato": q})

# -----------------------------------------------------
def detalle_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

# -----------------------------------------------------
@session_rol_permission(1, 3)
def eliminar_producto(request, id_producto):
    try:
        q = Producto.objects.get(pk=id_producto)
        q.delete()
        messages.success(request, 'Producto eliminado Correctamente...')
    except Producto.DoesNotExist:
        messages.warning(request, "Error: El producto no existe")
    except Exception as e:
        messages.error(request, f"Error {e}")
    return redirect("lista_productos")
