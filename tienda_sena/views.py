from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from decimal import Decimal
from .models import *
from .utils import *
from .templatetags.custom_filters import *



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
            return redirect("index")
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
    if request.session.get("pista"):
        messages.info(request, "Ya tienes una sesión activa. :)")
        return redirect("index") 
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

def perfil_usuario(request):
    if request.session.get("pista"):  # Verificar si hay una sesión activa
        usuario = request.session["pista"]  # Obtener los datos del usuario desde la sesión
        nombre_apellido = usuario.get("nombre") # Obtener el nombre completo del usuario
        correo = usuario.get("correo") #  Obtener el correo del usuario
        return render(request, "usuarios/perfil_usuario.html", {
            "nombre_apellido": nombre_apellido,  # Pasar el nombre al contexto
            "correo": correo, # Pasar el correo al contexto
        })
    else:
        messages.error(request, "Debes iniciar sesión para acceder a tu perfil.")
        return redirect("login")
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
        # Obtener datos del formulario
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio_original = request.POST.get("precio_original", "0")
        descuento = request.POST.get("descuento", "0")
        en_oferta = request.POST.get("en_oferta") == "on"
        stock = request.POST.get("stock")
        vendedor = request.POST.get("vendedor")
        categoria = request.POST.get("categoria")
        color = request.POST.get("color")
        imagenes = request.FILES.getlist("imagenes")

        try:
            # Crear el producto
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                precio_original=Decimal(precio_original),
                descuento=Decimal(descuento),
                en_oferta=en_oferta,
                stock=stock,
                vendedor_id=vendedor,
                categoria=int(categoria),
                color=color,
            )
            producto.save()

            # Guardar imágenes
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)
            messages.success(request, "Producto guardado correctamente!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("lista_productos")
    else:
        user = request.session.get("pista")
        roles = dict(Usuario.ROLES).get(user["rol"], "Desconocido")
        categorias = Producto.CATEGORIAS

        return render(request, "productos/agregar_productos.html", {
            'user': user,
            'roles': roles,
            'categorias': categorias,
        })
    
# -----------------------------------------------------

@session_rol_permission(1, 3)
def editar_producto(request, id_producto):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio_original = request.POST.get("precio_original")
        descuento = request.POST.get("descuento", "0")
        en_oferta = request.POST.get("en_oferta") == "on"
        stock = request.POST.get("stock")
        vendedor = request.POST.get("vendedor")
        categoria = request.POST.get("categoria")
        color = request.POST.get("color")
        imagenes = request.FILES.getlist("imagenes")

        try:
            # Obtener el producto a editar
            producto = Producto.objects.get(pk=id_producto)

            # Actualizar los campos del producto
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio_original = Decimal(precio_original) if precio_original else Decimal(0)
            producto.descuento = Decimal(descuento) if descuento else Decimal(0)
            producto.en_oferta = en_oferta
            producto.stock = stock
            producto.vendedor_id = vendedor
            producto.categoria = categoria
            producto.color = color

            producto.save()

            # Guardar las nuevas imágenes asociadas al producto
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto actualizado correctamente!")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("lista_productos")
    else:
        producto = Producto.objects.get(pk=id_producto)
        return render(request, "productos/agregar_productos.html", {"dato": producto})


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




# -----------------------------------------------------
#Admin
# -----------------------------------------------------

def panel_admin(request):
    return render(request, 'administrador/panel_admin.html')

#--------------USUARIOS-----------------------
def usuarios(request):

    q = Usuario.objects.all()
    contexto = { "data": q }
    return render(request, "administrador/usuarios/listar_usuarios.html", contexto)

def agregar_usuario(request):
    if request.method == "POST":
        nombre_apellido = request.POST.get("nombre")
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
            q = Usuario(
                nombre_apellido=nombre_apellido,
                correo=correo,
                password=password,
                rol=rol,
                imagen_perfil=imagen_perfil  # Si es 1 solo archivo
            )
            q.save()
            messages.success(request, "Usuario guardado correctamente!")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("usuarios")
    else:
        return render(request, "administrador/usuarios/agregar_usuarios.html")

def editar_usuario(request, id_usuario):
    if request.method == "POST":
        q = Usuario.objects.get(pk = id_usuario)
        # procesar datos
        nombre_apellido = request.POST.get("nombre")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol = request.POST.get("rol")
        try:
            q.nombre_apellido = nombre_apellido
            q.correo = correo
            q.password = password
            q.rol = rol
            q.save()
            messages.success(request, "Usuario actualizado correctamente!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("usuarios")
    else:
        q = Usuario.objects.get(pk = id_usuario)
        return render(request, "administrador/usuarios/agregar_usuarios.html", {"dato": q})


def eliminar_usuario(request, id_usuario):
    try:
        q = Usuario.objects.get(pk = id_usuario)
        q.delete()
        messages.success(request, 'Producto eliminado Correctamente...')
    except Usuario.DoesNotExist:
        messages.warning(request, "Error: El usuaro no existe")
    except Exception as e:
        messages.error(request, f"Error {e}")

    return redirect("usuarios")



def productos_por_categoria(request, categoria):
    try:
        # Convertir el valor de categoria a entero
        categoria = int(categoria)
        productos = Producto.objects.filter(categoria=categoria)
        # Obtener el nombre de la categoría
        categoria_nombre = dict(Producto.CATEGORIAS).get(categoria, "Categoría desconocida")
    except ValueError:
        # Si no es un entero, mostrar categoría desconocida
        productos = []

    contexto = {'productos': productos, 'categoria': categoria_nombre}
    return render(request, 'productos/productos_por_categoria.html', contexto)

#-------------PRODUCTOS------------------------

def productos(request):
    q = Producto.objects.all()
    contexto = { "data": q }
    return render(request, "administrador/productos/listar_productos.html", contexto)

