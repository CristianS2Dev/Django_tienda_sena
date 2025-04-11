from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from decimal import Decimal
from .models import *
from .utils import *
import re
import json
from django.http import JsonResponse
from .templatetags.custom_filters import *
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .utils import session_rol_permission
from django.contrib.auth.decorators import login_required






from django.core.exceptions import PermissionDenied 



from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
def index(request):
    q = Producto.objects.all()[:3]
    contexto = {'data': q,
                'mostrar_boton_agregar': False,
    }
    return render(request, 'index.html', contexto)



def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        try:
            q = Usuario.objects.get(correo=correo)
            if check_password(password, q.password):  # Verificar la contraseña
                # Autenticación: Creamos la variable de sesión
                request.session["pista"] = {
                    "id": q.id,
                    "rol": q.rol,
                    "nombre": q.nombre_apellido
                }
                messages.success(request, "Bienvenido!!")
                return redirect("index")
            else:
                raise Usuario.DoesNotExist
        except Usuario.DoesNotExist:
            # Autenticación: Vaciamos la variable de sesión
            request.session["pista"] = None
            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect("login")
    else:
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

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')


def correo_valido(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo) is not None

class CorreoInvalidoError(Exception):
    pass

def registrarse(request):
    if request.session.get("pista"):
        messages.info(request, "Ya tienes una sesión activa. :) ")
        return redirect("index") 
    if request.method == "POST":
        nombre_apellido = request.POST.get("nombre")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        valid_password = request.POST.get("valid_password")
        rol = 2
        
        try:
            
            if not correo_valido(correo):
                raise CorreoInvalidoError("Correo electrónico inválido")
            
            if password != valid_password:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect("registrarse")
            
            # Validar contraseña con una sola condición
            if not (re.search(r'[A-Z]', password) and 
                    re.search(r'[a-z]', password) and 
                    re.search(r'\d', password) and 
                    re.search(r'[!@#$%^&*(),.?":{}|<>-]', password) and 
                    4 <= len(password) <= 20):
                messages.error(request, "La contraseña debe tener entre 8 y 20 caracteres, al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.")
                return redirect("registrarse")
            
            # Crear el usuario si todo está correcto
            usuario = Usuario(
                nombre_apellido=nombre_apellido,
                correo=correo,
                password=password,
                rol=rol,
            )
            usuario.save()
            messages.success(request, "Usuario registrado correctamente!")
            return redirect("login")
        except CorreoInvalidoError:
            messages.error(request, 'Error, el correo no es valido')
            return redirect("registrarse")  
        except IntegrityError:
            messages.error(request, "Error: El correo ya está registrado")
            return redirect("registrarse")
        except Usuario.DoesNotExist:
            messages.error(request, "Error: El usuario ya existe")
            return redirect("registrarse")
        
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("registrarse")
    else:
        return render(request, "registrarse.html")


def perfil_usuario(request):
    q = Usuario.objects.get(pk=request.session["pista"]["id"])
    if request.session.get("pista"):  # Verificar si hay una sesión activa
        return render(request, "usuarios/perfil_usuario.html", {
            "dato": q,
        })
    else:
        messages.error(request, "Debes iniciar sesión para acceder a tu perfil.")
        return redirect("login")
    
def perfil_usuario_id(request, id_usuario):
    q = Usuario.objects.get(pk=id_usuario)
    return render(request, "usuarios/perfil_usuario.html",{
        
        "dato": q,
    })




def actualizar_perfil(request):
    if not request.session.get("pista") or not request.session["pista"].get("id"):
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("login")

    usuario = Usuario.objects.get(pk=request.session["pista"]["id"])  # Obtener el usuario autenticado
    if request.method == "POST":
        nombre_apellido = request.POST.get("nombre")
        contacto = request.POST.get("contacto")
        direccion = request.POST.get("direccion")
        imagen_perfil = request.FILES.get("imagen_perfil")

        try:
            if imagen_perfil:
                validar_archivo(imagen_perfil)
                validar_tamano_archivo(imagen_perfil)
                usuario.imagen_perfil = imagen_perfil  # Actualizar la imagen de perfil

            usuario.nombre_apellido = nombre_apellido
            usuario.contacto = contacto
            usuario.direccion = direccion
            usuario.save()
            messages.success(request, "Perfil actualizado correctamente!")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("perfil_usuario")
    else:
        return render(request, "usuarios/actualizar_perfil.html", {"usuario": usuario})


def validar_archivo(imagen):
    """Valida el tipo de archivo permitido."""
    formatos_permitidos = ["image/jpeg", "image/png", "image/webp"]
    if imagen.content_type not in formatos_permitidos:
        raise ValidationError(f"Formato no permitido: {imagen.content_type}. Solo se aceptan JPEG, PNG o WEBP.")

def validar_tamano_archivo(imagen, max_size_mb=5):
    """Valida el tamaño del archivo subido."""
    if imagen.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"El archivo excede el tamaño máximo permitido de {max_size_mb} MB.")


    

def validar_imagen(imagen, max_size_mb=5):
    """Valida el tipo, tamaño y seguridad del archivo."""
    try:
        validar_archivo(imagen)
        validar_tamano_archivo(imagen, max_size_mb)
    except ValidationError as ve:
        raise ValidationError(f"Error de validación: {ve}")
    except Exception as e:
        raise Exception(f"Error al escanear archivo: {e}")


        
# -----------------------------------------------------  
        #CRUD Listar productos usuario
# -----------------------------------------------------

def lista_productos(request):
    q = Producto.objects.all()
    contexto = {'data': q,
                'mostrar_boton_agregar': True,
    }
    return (render(request, 'productos/listar_productos.html', contexto))

def productos_vendedor(request, id_vendedor):
    productos = Producto.objects.filter(vendedor_id=id_vendedor)
    contexto = {'data': productos}
    return render(request, 'productos/listar_productos.html', contexto)

def detalle_producto_admin(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    return render(request, 'administrador/productos/detalle_producto_admin.html', {'producto': producto})


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
            if precio_original < 0:
                messages.error(request, "El precio original no puede ser negativo.")
            if descuento < 0 or descuento > 100:
                 messages.error(request,"El descuento debe estar entre 0 y 100.")
            if stock < 0:
                 messages.error(request,"El stock no puede ser negativo.")

            # Validar y procesar imágenes
            for imagen in imagenes:
                try:
                    validar_archivo(imagen)
                    validar_tamano_archivo(imagen)
                except ValidationError as ve:
                    messages.error(request, f"Error de validación: {ve}")
                    return redirect("agregar_producto")
                except Exception as e:
                    messages.error(request, f"Error al escanear archivo: {e}")
                    return redirect("agregar_producto")

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
            producto.full_clean()
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
        rol = request.session.get("pista")["rol"]

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

            for imagen in imagenes:
                try:
                    validar_archivo(imagen)
                    validar_tamano_archivo(imagen)
                except ValidationError as ve:
                    messages.error(request, f"Error de validación: {ve}")
                    return redirect("editar_producto", id_producto=id_producto)
                except Exception as e:
                    messages.error(request, f"Error al escanear archivo: {e}")
                    return redirect("editar_producto", id_producto=id_producto)

            producto.full_clean()
            producto.save()
            # Guardar las nuevas imágenes asociadas al producto
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto actualizado correctamente!")
            if rol == 1:
                return redirect("productos") 
            else:    
                return redirect("lista_productos") 
            
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        producto = Producto.objects.get(pk=id_producto)
        return render(request, "productos/agregar_productos.html", {"dato": producto})


def detalle_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    rango_cantidad = range(1, producto.stock + 1)  # Generar el rango basado en el stock
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'rango_cantidad': rango_cantidad
    })

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

# -----------------------------------------------------
# -----------------------------------------------------



# -----------------------------------------------------
                #ADMINISTRADOR
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
        documento = request.POST.get("documento")
        contacto = request.POST.get("contacto")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol = request.POST.get("rol")
        imagen_perfil = request.FILES.get("imagen_perfil")  # Obtener la imagen del formulario
        direccion = request.POST.get("direccion")

        try:
            if imagen_perfil:
                try:
                    validar_archivo(imagen_perfil) 
                    validar_tamano_archivo(imagen_perfil) 
                except ValidationError as ve:
                    messages.error(request, f"Error de validación: {ve}")
                    return redirect("agregar_usuario")
                except Exception as e:
                    messages.error(request, f"Error al escanear archivo: {e}")
                    return redirect("agregar_usuario")

            # Crear el usuario
            q = Usuario(
                nombre_apellido=nombre_apellido,
                documento=documento,
                contacto=contacto,
                correo=correo,
                password=password,
                rol=rol,
                imagen_perfil=imagen_perfil,  # Guardar la imagen si es válida
                direccion=direccion
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
        documento = request.POST.get("documento")
        contacto = request.POST.get("contacto")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol = request.POST.get("rol")
        imagen_perfil=imagen_perfil,
        direccion = request.POST.get("direccion")
        try:
            if imagen_perfil:
                try:
                    validar_archivo(imagen_perfil) 
                    validar_tamano_archivo(imagen_perfil) 
                except ValidationError as ve:
                    messages.error(request, f"Error de validación: {ve}")
                    return redirect("agregar_usuario")
                except Exception as e:
                    messages.error(request, f"Error al escanear archivo: {e}")
                    return redirect("agregar_usuario")

            q.nombre_apellido = nombre_apellido
            q.documento = documento
            q.contacto = contacto
            q.correo = correo
            q.password = password
            q.rol = rol
            q.imagen_perfil = imagen_perfil
            q.direccion = direccion
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
        # respuesta = request.POST.get('confirmar_eliminar_usuario')        
        q = Usuario.objects.get(pk=id_usuario)  
        if q.rol != 1:# and respuesta == 'acepto'
            q.delete()
            messages.success(request, 'Usuario eliminado Correctamente...')
        else:
            messages.error(request,"No puedes eliminar un administrador" )
    except Usuario.DoesNotExist:
        messages.warning(request, "Error: El usuaro no existe")
    except Exception as e:
        messages.error(request, f"Error {e}")

    return redirect("usuarios")

# -----------------------------------------------------
# -----------------------------------------------------

#-------------PRODUCTOS------------------------

def productos_admnin(request):
    q = Producto.objects.all()
    contexto = { "data": q }
    return render(request, "administrador/productos/listar_productos.html", contexto)

def modulo_tienda(request):
    return render(request, 'productos/tienda.html')



# ---------------------------------------------
    ## Carrito de compras
# ---------------------------------------------

def obtener_carrito(request):
    """Obtiene el carrito del usuario autenticado o de la sesión."""
    if request.user.is_authenticated:
        # Convertir request.user a una instancia del modelo Usuario personalizado
        usuario = Usuario.objects.filter(correo=request.user.email).first()
        if not usuario:
            # Lanzar una excepción si el usuario no está registrado en el modelo Usuario
            raise ValueError("El usuario autenticado no está registrado como Usuario en el sistema.")
        
        # Si el usuario está autenticado, usa su carrito
        carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    else:
        # Si no está autenticado, usa un carrito basado en la sesión
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id).first()
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    return carrito


def agregar_carrito(request, id_producto):
    """Agrega un producto al carrito."""
    try:
        carrito = obtener_carrito(request)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('login')  # Redirigir al login si no se puede obtener el carrito

    producto = get_object_or_404(Producto, id=id_producto)
    cantidad = int(request.POST.get('cantidad', 1))
    
    # Validar cantidad
    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser mayor a 0.")
        return redirect('carrito')
    if cantidad > producto.stock:
        messages.error(request, "La cantidad excede el stock disponible.")
        return redirect('carrito')
    
    # Buscar o crear el elemento en el carrito
    elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        elemento.cantidad += cantidad  # Incrementar la cantidad si ya existe
    else:
        elemento.cantidad = cantidad  # Establecer la cantidad si es un nuevo elemento
    elemento.save()
    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect('carrito')

def carrito(request):
    """Muestra el carrito del usuario."""
    carrito = obtener_carrito(request)
    elementos = carrito.elementos.all()  # Obtener todos los elementos del carrito
    total = sum(elemento.producto.precio * elemento.cantidad for elemento in elementos)  # Calcular el total en el servidor

    contexto = {
        'elementos': elementos,
        'total': total,
    }
    return render(request, 'productos/carrito/carrito.html', contexto)


def eliminar_del_carrito(request, id_elemento):
    """Elimina un producto del carrito."""
    carrito = obtener_carrito(request)
    elemento = get_object_or_404(ElementoCarrito, id=id_elemento, carrito=carrito)
    elemento.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('carrito')


def actualizar_carrito(request, id_elemento):
    """Actualiza la cantidad de un producto en el carrito."""
    if request.method == 'POST':
        carrito = obtener_carrito(request)
        elemento = get_object_or_404(ElementoCarrito, id=id_elemento, carrito=carrito)
        nueva_cantidad = int(request.POST.get('cantidad', 1))

        if nueva_cantidad <= 0:
            elemento.delete()
            return JsonResponse({'subtotal': 0, 'total': carrito.total()})

        if nueva_cantidad > elemento.producto.stock:
            return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)

        # Recalcular el subtotal en el servidor
        elemento.cantidad = nueva_cantidad
        elemento.save()
        subtotal = elemento.producto.precio * elemento.cantidad
        total = sum(
            e.producto.precio * e.cantidad for e in carrito.elementos.all()
        )
        return JsonResponse({
            'subtotal': subtotal,
            'total': total
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)



from django.db.models import F

@session_rol_permission()
def pagar_carrito(request):
    """Procesa el pago del carrito."""
    carrito = obtener_carrito(request)

    # Verificar si el carrito está vacío
    if not carrito.elementos.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('carrito')

    # Aquí iría la lógica de procesamiento del pago
    messages.success(request, "Pago procesado correctamente.")
    #  mostrar mensaje con el valor de la compra 
    total = sum(elemento.producto.precio * elemento.cantidad for elemento in carrito.elementos.all())
    # Actualizar el stock de los productos
    for elemento in carrito.elementos.all():
        producto = elemento.producto
        producto.stock = F('stock') - elemento.cantidad
        producto.save()
        elemento.delete()
    # Limpiar el carrito después del pago
    carrito.elementos.all().delete()  # Vaciar el carrito después del pago
    return redirect('index')


def combinar_carritos(request):
    if request.user.is_authenticated:
        session_carrito_id = request.session.get('carrito_id')
        if session_carrito_id:
            session_carrito = Carrito.objects.filter(id=session_carrito_id).first()
            user_carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            if session_carrito:
                for elemento in session_carrito.elementos.all():
                    elemento.carrito = user_carrito
                    elemento.save()
                session_carrito.delete()
            del request.session['carrito_id']

# ---------------------------------------------
# ---------------------------------------------


# ---------------------------------------------
    # Busqueda de productos
# ---------------------------------------------


def buscar_productos(request):
    query = request.GET.get('q', '')  # Obtén el término de búsqueda
    resultados = Producto.objects.filter(nombre__icontains=query) if query else []
    contexto = {
        'data': resultados,  # Pasar los productos encontrados
        'query': query,
        'mostrar_boton_agregar': False,  # Opcional: Ocultar el botón de agregar
    }
    return render(request, 'productos/resultados_busqueda.html', contexto)

