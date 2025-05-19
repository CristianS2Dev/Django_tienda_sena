from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from decimal import Decimal
from .models import *
from .utils import *
import re
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .templatetags.custom_filters import *
from django.contrib.auth.hashers import check_password
from .utils import session_rol_permission
from django.db.models import F
from django.contrib import messages
from django.db import IntegrityError
from django.db import transaction
from django.urls import reverse
from django.core.mail import send_mail
import random


# Create your views here.
def index(request):
    """Vista principal de la tienda."""
    q = Producto.objects.all()[:6]
    pendientes = 0
    if request.session.get("pista",{}).get("rol") == 1:
        # Si el usuario es administrador, contar las solicitudes pendientes
        pendientes = SolicitudVendedor.objects.filter(estado="pendiente").count()
    contexto = {'data': q,
                'mostrar_boton_agregar': False,
                 "pendientes_solicitudes_vendedor": pendientes,
    }
    return render(request, 'index.html', contexto)



def login(request):
    """Vista para iniciar sesión."""
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
                combinar_carritos(request)
                messages.success(request, "Bienvenido " + q.nombre_apellido + "!")
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
    """Vista para cerrar sesión."""
    try:
        del request.session["pista"]
        return redirect("index")
    except:
        messages.error(request, "Ocurrio un error")
        return redirect("index")

def sobre_nosotros(request):
    """Vista para la sección 'Sobre nosotros'."""
    return render(request, 'sobre_nosotros.html')


def correo_valido(correo):
    """ Valida el formato del correo electrónico. """
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo) is not None

class CorreoInvalidoError(Exception):
    pass

def validar_contraseña(password):
    """ Valida la contraseña según los criterios establecidos. """
    if not password:
        return False, "La contraseña no puede estar vacía."
    
    if not (8 <= len(password) <= 20):
        return False, "La contraseña debe tener entre 8 y 20 caracteres."
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula."
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número."
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>-]', password):
        return False, "La contraseña debe contener al menos un carácter especial."
    
    contraseñas_comunes = [
        "123456", "password", "123456789", "qwerty", "abc123", "111111", "123123", "12345", "12345678", "admin"
    ]
    if password.lower() in contraseñas_comunes:
        return False, "La contraseña es demasiado común. Elige una más segura."
    
    return True, "Contraseña válida."

def olvidar_contraseña(request):

    if request.method == "POST":
        correo = request.POST.get("correo")
        try:
            usuario = Usuario.objects.get(correo=correo)

            # Aquí puedes implementar el envío de un correo electrónico para restablecer la contraseña
            messages.success(request, "Se ha enviado un enlace para restablecer tu contraseña a tu correo.")
            return redirect("login")
        except Usuario.DoesNotExist:
            messages.error(request, "El correo no está registrado.")
            return redirect("olvidar_contraseña")
    else:
        return render(request, "olvidar_contraseña.html")

@csrf_exempt  # Solo para pruebas, en producción usa el token CSRF correctamente
def ajax_enviar_codigo(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        correo = data.get("correo")
        if not correo:
            return JsonResponse({"ok": False, "msg": "Correo requerido."})
        try:
            usuario = Usuario.objects.get(correo=correo)
            # Generar un código aleatorio de 6 dígitos
            codigo = random.randint(100000, 999999)

            # Guardar el código en la base de datos asociado al usuario
            usuario.codigo_verificacion = codigo
            usuario.save()

            # Enviar el correo con el código
            send_mail(
                'Código de verificación',
                f'Tu código de verificación es: {codigo}',
                'tiendasenaccc@gmail.com',  
                [correo],
                fail_silently=False,
            )
            return JsonResponse({"ok": True, "msg": "Código enviado al correo."})
        except Usuario.DoesNotExist:
            return JsonResponse({"ok": False, "msg": "El correo no está registrado."})
    return JsonResponse({"ok": False, "msg": "Método no permitido."}, status=405)

def registrarse(request):
    """Vista para el registro de nuevos usuarios."""
    if request.session.get("pista"):
        messages.info(request, "Ya tienes una sesión activa. :) ")
        return redirect("index") 
    if request.method == "POST":
        nombre_apellido = request.POST.get("nombre")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        valid_password = request.POST.get("valid_password")
        rol = 2

        campos = {
            "nombre": nombre_apellido,
            "correo": correo,
            "password": password,
            "valid_password": valid_password,
        }
        
        try:
            if not correo_valido(correo):
                raise CorreoInvalidoError("Correo electrónico inválido")
            
            if password != valid_password:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, "registrarse.html", campos)
            
            es_valida, mensaje = validar_contraseña(password)
            if not es_valida:
                messages.error(request, mensaje)
                return render(request, "registrarse.html", campos)
            
            usuario = Usuario(
                nombre_apellido=nombre_apellido,
                correo=correo,
                password=make_password(password),
                rol=rol,
            )
            usuario.save()
            messages.success(request, "Usuario registrado correctamente!")
            return redirect("login")
        except CorreoInvalidoError:
            messages.error(request, 'Error, el correo no es valido')
            return render(request, "registrarse.html", campos)
        except IntegrityError:
            messages.error(request, "Error: El correo ya está registrado")
            return render(request, "registrarse.html", campos)
        except Usuario.DoesNotExist:
            messages.error(request, "Error: El usuario ya existe")
            return render(request, "registrarse.html", campos)
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, "registrarse.html", campos)
    else:
        return render(request, "registrarse.html")

def perfil_usuario(request):
    """Vista para mostrar el perfil del usuario autenticado."""
    q = Usuario.objects.get(pk=request.session["pista"]["id"])
    solicitud_pendiente = SolicitudVendedor.objects.filter(usuario=q).order_by('-fecha_solicitud').first()

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", None),
    ]

    if request.session.get("pista"):
        return render(request, "usuarios/perfil_usuario.html", {
            "dato": q,
            "direccion_principal": Direccion.objects.filter(usuario=q, principal=True).first(),
            "solicitud_pendiente": solicitud_pendiente,
            "breadcrumbs": breadcrumbs,
        })
    else:
        messages.error(request, "Debes iniciar sesión para acceder a tu perfil.")
        return redirect("login")
    
def perfil_usuario_id(request, id_usuario):
    """Vista para mostrar el perfil de un usuario específico."""
    q = Usuario.objects.get(pk=id_usuario)
    breadcrumbs = [
        ("Inicio Admin", reverse("panel_admin")),
        ("lista de usuarios", reverse("usuarios")),
        (q.nombre_apellido, reverse("perfil_usuario_id", args=[q.id])),
    ]
    return render(request, "usuarios/perfil_usuario.html",{
        
        "dato": q,
        "breadcrumbs": breadcrumbs,
    })



def actualizar_perfil(request):
    """Vista para actualizar el perfil del usuario autenticado."""
    usuario = Usuario.objects.get(pk=request.session["pista"]["id"])  # Obtener el usuario autenticado
    if request.method == "POST":
        nombre_apellido = request.POST.get("nombre")
        contacto = request.POST.get("contacto")
        imagen_perfil = request.FILES.get("imagen_perfil")
        try:
            if imagen_perfil:
                validar_archivo(imagen_perfil)
                validar_tamano_archivo(imagen_perfil)
                usuario.imagen_perfil = imagen_perfil 
                
            usuario.nombre_apellido = nombre_apellido
            usuario.contacto = contacto
            
            usuario.save()
            messages.success(request, "Perfil actualizado correctamente!")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("perfil_usuario")
    else:
        direccion_principal = Direccion.objects.filter(usuario=usuario, principal=True).first()
        return render(
            request,
            "usuarios/actualizar_perfil.html",
            {
                "usuario": usuario,
                "direccion_principal": direccion_principal,
            }
        )

def actualizar_contraseña(request):
    """Vista para actualizar la contraseña del usuario autenticado."""
    usuario = Usuario.objects.get(pk=request.session["pista"]["id"])
    if request.method == "POST":
        password = request.POST.get("password")
        new_password = request.POST.get("new_password") 
        confirm_new_password = request.POST.get("confirm_new_password")
        
        try:
            # Verificar la contraseña actual
            if not check_password(password, usuario.password):
                messages.error(request, "La contraseña actual es incorrecta.")
                return redirect("actualizar_contraseña")
            
            # Verificar que las nuevas contraseñas coincidan
            if new_password != confirm_new_password:
                messages.error(request, "Las nuevas contraseñas no coinciden.")
                return redirect("actualizar_contraseña")
            
            # Validar la nueva contraseña
            es_valida, mensaje = validar_contraseña(new_password)
            if not es_valida:
                messages.error(request, "la contraseña no es valida!")
                return redirect("actualizar_contraseña")
            
            # Actualizar la contraseña encriptada
            usuario.password = make_password(new_password)
            usuario.save()
            messages.success(request, "Contraseña actualizada correctamente!")
            return redirect("perfil_usuario")
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("actualizar_contraseña")
    else:
        return render(request, "usuarios/actualizar_contraseña.html", {"usuario": usuario})
    

@session_rol_permission(2)
def solicitar_vendedor(request):
    usuario = Usuario.objects.get(pk=request.session["pista"]["id"])
    ultima_solicitud = SolicitudVendedor.objects.filter(usuario=usuario).order_by('-fecha_solicitud').first()
    if ultima_solicitud and ultima_solicitud.estado == 'pendiente':
        messages.info(request, "Ya tienes una solicitud pendiente.")
        return redirect("perfil_usuario")
    if request.method == "POST":
        certificado = request.FILES.get("certificado_sena")
        if not certificado:
            messages.error(request, "Debes adjuntar tu certificado.")
            return redirect("solicitar_vendedor")
        SolicitudVendedor.objects.create(usuario=usuario, certificado=certificado)
        messages.success(request, "Solicitud enviada. Un administrador la revisará.")
        return redirect("perfil_usuario")
    return render(request, "usuarios/solicitar_vendedor.html")


# -----------------------------------------------------
    #DIRECCION
#-----------------------------------------------------


@session_rol_permission()
def direccion_usuario(request):
    """Muestra la dirección del usuario autenticado."""
    try:
        usuario = Usuario.objects.get(id=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login_usuario')
    
    direcciones = Direccion.objects.filter(usuario=usuario)
    
    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("perfil_usuario")),
        ("Dirección", None)
    ]

    context = {
        'usuario': usuario,
        'breadcrumbs': breadcrumbs,
        'direcciones': direcciones,
    }
    return render(request, 'usuarios/direccion_usuario.html', context)


def agregar_direccion(request):
    """"Agrega una nueva dirección para el usuario autenticado."""
    try:
        usuario = Usuario.objects.get(id=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('login')

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("perfil_usuario")),
        ("Dirección", reverse("direccion_usuario")),
        ("Agregar Dirección", None)
    ]

    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        estado = request.POST.get('estado')
        codigo_postal = request.POST.get('codigo_postal')
        pais = request.POST.get('pais')
        principal = request.POST.get('principal') == 'on'  # Verifica si el checkbox está marcado

        try:
            # Validar los datos de la dirección
            validar_direccion(direccion, ciudad, estado, codigo_postal, pais)
            if Direccion.objects.filter(
                usuario=usuario,
                direccion=direccion,
                ciudad=ciudad,
                estado=estado,
                codigo_postal=codigo_postal,
                pais=pais
            ).exists():
                raise ValidationError("Ya tienes registrada esta dirección.")
            
            # Crear la dirección
            nueva_direccion = Direccion.objects.create(
                usuario=usuario,
                direccion=direccion,
                ciudad=ciudad,
                estado=estado,
                codigo_postal=codigo_postal,
                pais=pais,
                principal=principal
            )
            messages.success(request, 'Dirección agregada correctamente.')
            return redirect('direccion_usuario')
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")


        # Si hay un error, devolver los datos ingresados al formulario
        return render(request, 'usuarios/agregar_direccion_usuario.html', {
            'breadcrumbs': breadcrumbs,
            'direccion_valor': direccion,
            'ciudad_valor': ciudad,
            'estado_valor': estado,
            'codigo_postal_valor': codigo_postal,
            'pais_valor': pais,
            'principal_valor': principal,
        })

    # Para solicitudes GET, pasar valores vacíos al formulario
    return render(request, 'usuarios/agregar_direccion_usuario.html', {
        'breadcrumbs': breadcrumbs,
        'direccion_valor': '',
        'ciudad_valor': '',
        'estado_valor': '',
        'codigo_postal_valor': '',
        'pais_valor': '',
        'principal_valor': False,
    })


@session_rol_permission()
def editar_direccion(request,id_direccion):
    """"Actualiza una dirección existente del usuario autenticado."""
    try:
        direccion = Direccion.objects.get(id=id_direccion, usuario__id=request.session['pista']['id'])
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección no encontrada.")
        return redirect('direccion_usuario')

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Mi cuenta", reverse("perfil_usuario")),
        ("Dirección", reverse("direccion_usuario")),
        ("Actualizar Dirección", None)
    ]

    if request.method == 'POST':
        direccion.direccion = request.POST.get('direccion')
        direccion.ciudad = request.POST.get('ciudad')
        direccion.estado = request.POST.get('estado')
        direccion.codigo_postal = request.POST.get('codigo_postal')
        direccion.pais = request.POST.get('pais')
        direccion.principal = request.POST.get('principal') == 'on'  # Verifica si el checkbox está marcado
        try:
            if Direccion.objects.filter(
                usuario=direccion.usuario,
                direccion=direccion.direccion,
                ciudad=direccion.ciudad,
                estado=direccion.estado,
                codigo_postal=direccion.codigo_postal,
                pais=direccion.pais
            ).exclude(id=direccion.id).exists():
                raise ValidationError("Ya tienes registrada esta dirección.")
            validar_direccion(direccion.direccion, direccion.ciudad, direccion.estado, direccion.codigo_postal, direccion.pais)

            # Guardar los cambios
            direccion.save()
            messages.success(request, 'Dirección actualizada correctamente.')
            return redirect('direccion_usuario')
        except ValidationError as ve:
            messages.error(request, f"Error de validación: {ve}")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")

    return render(request, 'usuarios/agregar_direccion_usuario.html', {
        'breadcrumbs': breadcrumbs,
        'direccion': direccion,
        'direccion_valor': direccion.direccion,
        'ciudad_valor': direccion.ciudad,
        'estado_valor': direccion.estado,
        'codigo_postal_valor': direccion.codigo_postal,
        'pais_valor': direccion.pais,
        'principal_valor': direccion.principal,
    })

def set_primary_address(request, id_address):
    """Establece una dirección como principal."""
    try:
        direccion = Direccion.objects.get(id=id_address, usuario__id=request.session['pista']['id'])
        Direccion.objects.filter(usuario=direccion.usuario).update(principal=False)
        direccion.principal = True
        direccion.save()
        messages.success(request, 'Dirección establecida como principal.')
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección no encontrada.")
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
    return redirect('address')

def eliminar_direccion(request, id):
    """"Elimina una dirección existente del usuario autenticado."""
    try:
        direccion = Direccion.objects.get(id=id, usuario__id=request.session['pista']['id'])
        direccion.delete()
        messages.success(request, 'Dirección eliminada correctamente.')
    except Direccion.DoesNotExist:
        messages.error(request, "Dirección no encontrada.")
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
    return redirect('direccion_usuario')



#------------------------------------------------------
    # FIN DIRECCION
#------------------------------------------------------



# -----------------------------------------------------
    #VALIDACIONES
# -----------------------------------------------------

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


def validar_direccion(direccion, ciudad, estado, codigo_postal, pais):
    """Valida los campos de una dirección."""
    if not all([direccion, ciudad, estado, codigo_postal, pais]):
        raise ValidationError("Todos los campos son obligatorios.")
    if not codigo_postal.isdigit() or len(codigo_postal) != 6:
        raise ValidationError("El código postal debe ser un número de 5 dígitos.")

# -----------------------------------------------------
    # FIN VALIDACIONES
#-----------------------------------------------------


# -----------------------------------------------------  
        #CRUD Listar productos usuario
# -----------------------------------------------------

def lista_productos(request, id_categoria=None):
    """
    Vista para mostrar la lista de productos con filtros opcionales.
    Si se proporciona una categoría, filtra los productos por esa categoría.
    """
    productos = Producto.objects.all()

    # Obtener colores y categorías disponibles del modelo Producto
    colores_disponibles = Producto.COLORES
    categorias_disponibles = Producto.CATEGORIAS
    colores_disponibles = Producto.COLORES
    categoria = request.GET.get('categoria')
    
    if categoria:
        try:
            categoria = int(categoria)
            productos = productos.filter(categoria=categoria)
            categoria_obj = next((c for c in categorias_disponibles if c[0] == categoria), None)
        except (ValueError, TypeError):
            categoria_obj = None

    COLOR_CODES = {
        "Gris": "#808080",
        "Blanco": "#ffffff",
        "Negro": "#000000",
        "Amarillo": "#ffff00",
        "Azul": "#0000ff",
        "Rojo": "#ff0000",
    }

    colores_con_codigo = []
    for color in colores_disponibles:
        if color[0] != 0:
            colores_con_codigo.append({
                "id": color[0],
                "nombre": color[1],
                "codigo": COLOR_CODES.get(color[1], "#cccccc")
            })

    categoria = None
    categoria_obj = None
    if id_categoria is not None:
        try:
            id_categoria = int(id_categoria)
            categoria = id_categoria
            productos = productos.filter(categoria=id_categoria)
            # Obtener el objeto de la categoría
            categoria_obj = next((c for c in categorias_disponibles if c[0] == id_categoria), None)
        except (ValueError, TypeError):
            categoria = None
            categoria_obj = None

    nombre = request.GET.get('nombre')
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)

    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        try:
            productos = productos.filter(precio_original__gte=float(precio_min))
        except ValueError:
            pass
    if precio_max:
        try:
            productos = productos.filter(precio_original__lte=float(precio_max))
        except ValueError:
            pass

    colores = request.GET.getlist('color')
    if colores:
        try:
            colores_int = [int(c) for c in colores]
            productos = productos.filter(color__in=colores_int)
        except ValueError:
            pass

    # Ordenar productos
    orden = request.GET.get('orden')
    if orden == 'popular':
        productos = productos.order_by('-id') # Suponiendo que los productos más recientes son los más populares
    elif orden == 'barato':
        productos = productos.order_by('precio_original')
    elif orden == 'caro':
        productos = productos.order_by('-precio_original')

    # Paginación
    from django.core.paginator import Paginator

    paginator = Paginator(productos, 9)  # 9 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'data': page_obj,
        'categoria': categoria_obj,
        'categorias': categorias_disponibles,
        'colores_disponibles': colores_disponibles,
        'colores_con_codigo': colores_con_codigo,
    }
    return render(request, 'productos/listar_productos.html', contexto)


def productos_vendedor(request, id_vendedor):
    """Vista para mostrar los productos de un vendedor específico."""
    productos = Producto.objects.filter(vendedor_id=id_vendedor)
    contexto = {'data': productos}
    return render(request, 'productos/listar_productos.html', contexto)

def detalle_producto_admin(request, id_producto):
    """Vista para mostrar los detalles de un producto específico."""
    producto = get_object_or_404(Producto, id=id_producto)
    breadcrumbs = [
        ("Inicio Admin", reverse("panel_admin")),
        ("Lista de productos", reverse("productos_admnin")),
        (producto.nombre, None),
    ]
    contexto = {
        'producto': producto,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'administrador/productos/detalle_producto_admin.html', contexto)


@session_rol_permission(1, 3)
def agregar_producto(request):
    """Vista para agregar un nuevo producto."""
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

            if len(imagenes) > 5:
                messages.error(request, "Solo puedes subir hasta 5 imágenes por producto.")
                return redirect("agregar_producto")

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
    """Vista para editar un producto existente."""
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
                return redirect("productos_admnin") 
            else:    
                return redirect("lista_productos") 
            
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
            return redirect("lista_productos")  # <-- Añade este return
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("editar_producto", id_producto=id_producto)  # <-- Añade este return
    else:
        producto = Producto.objects.get(pk=id_producto)
        return render(request, "productos/agregar_productos.html", {"dato": producto})

def detalle_producto(request, id_producto):
    """Vista para mostrar los detalles de un producto específico."""
    producto = get_object_or_404(Producto, id=id_producto)
    rango_cantidad = range(1, producto.stock + 1)
    COLOR_CODES = {
        1: "#808080",   # Gris
        2: "#ffffff",   # Blanco
        3: "#000000",   # Negro
        4: "#ffff00",   # Amarillo
        5: "#0000ff",   # Azul
        6: "#ff0000",   # Rojo
    }
    color_codigo = COLOR_CODES.get(producto.color, "#cccccc")
    color_nombre = dict(Producto.COLORES).get(producto.color, "Ninguno")

    breadcrumbs = [
        ("Inicio", reverse("index")),
        ("Productos", reverse("lista_productos")),
        (producto.nombre, None),
    ]
    contexto = {
        'producto': producto,
        'rango_cantidad': rango_cantidad,
        'color_codigo': color_codigo,
        'color_nombre': color_nombre,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'productos/detalle_producto.html', contexto)

@session_rol_permission(1, 3)
def eliminar_producto(request, id_producto):
    """Vista para eliminar un producto."""
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
    # FIN CRUD Listar productos usuario
# -----------------------------------------------------


# -----------------------------------------------------
                #ADMINISTRADOR
# -----------------------------------------------------
@session_rol_permission(1)
def panel_admin(request):
    """Vista para el panel de administración."""
    breadcrumbs = [
        ("Inicio Admin", None),
    ]
    contexto = {
        "breadcrumbs": breadcrumbs,
    }
    return render(request, 'administrador/panel_admin.html', contexto)

#-----------------------------------------------------
    # USUARIOS ADMINISTRADOR
#-----------------------------------------------------
@session_rol_permission(1)
def usuarios(request):
    """Vista para mostrar la lista de usuarios."""
    q = Usuario.objects.all()
    breadcrumbs = [
        ("Inicio Admin", reverse("panel_admin")),
        ("Lista de usuarios", None),
    ]
    contexto = { "data": q,
                "breadcrumbs": breadcrumbs,
    }
    return render(request, "administrador/usuarios/listar_usuarios.html", contexto)

@session_rol_permission(1)
def agregar_usuario(request):
    """Vista para agregar un nuevo usuario."""
    if request.method == "POST":
        nombre_apellido = request.POST.get("nombre")
        documento = request.POST.get("documento")
        contacto = request.POST.get("contacto")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol = request.POST.get("rol")
        imagen_perfil = request.FILES.get("imagen_perfil")  # Obtener la imagen del formulario

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
                password=make_password(password),
                rol=rol,
                imagen_perfil=imagen_perfil,  # Guardar la imagen si es válida
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

@session_rol_permission(1)
def editar_usuario(request, id_usuario):
    """Vista para editar un usuario existente."""
    if request.method == "POST":
        q = Usuario.objects.get(pk=id_usuario)
        # procesar datos
        nombre_apellido = request.POST.get("nombre")
        documento = request.POST.get("documento")
        contacto = request.POST.get("contacto")
        correo = request.POST.get("correo")
        password = request.POST.get("password")
        rol = request.POST.get("rol")
        imagen_perfil = request.FILES.get("imagen_perfil")
        try:
            if imagen_perfil:
                try:
                    validar_archivo(imagen_perfil) 
                    validar_tamano_archivo(imagen_perfil)
                    q.imagen_perfil = imagen_perfil
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
            q.password = make_password(password)
            q.rol = rol
            q.save()
            messages.success(request, "Usuario actualizado correctamente!")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect("usuarios")
    else:
        q = Usuario.objects.get(pk=id_usuario)
        return render(request, "administrador/usuarios/agregar_usuarios.html", {"dato": q})

@session_rol_permission(1)
def eliminar_usuario(request, id_usuario):
    """Vista para eliminar un usuario."""
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


@session_rol_permission(1)
def solicitudes_vendedor(request):
    solicitudes = SolicitudVendedor.objects.filter(estado='pendiente')
    return render(request, "administrador/usuarios/solicitudes/solicitudes_vendedor.html", {"solicitudes": solicitudes})

@session_rol_permission(1)
def aprobar_solicitud_vendedor(request, id_solicitud):
    solicitud = SolicitudVendedor.objects.get(pk=id_solicitud)
    solicitud.estado = 'aprobado'
    solicitud.usuario.rol = 3  # Cambia a vendedor
    solicitud.usuario.save()
    solicitud.save()
    messages.success(request, "Solicitud aprobada y usuario actualizado a vendedor.")
    return redirect("solicitudes_vendedor")

@session_rol_permission(1)
def rechazar_solicitud_vendedor(request, id_solicitud):
    solicitud = SolicitudVendedor.objects.get(pk=id_solicitud)
    solicitud.estado = 'rechazado'
    solicitud.save()
    messages.info(request, "Solicitud rechazada.")
    return redirect("solicitudes_vendedor")


#-----------------------------------------------------
    # FIN USUARIOS ADMINISTRADOR
#-----------------------------------------------------

#-----------------------------------------------------
    # PRODUCTOS ADMINISTRADOR
#-----------------------------------------------------
@session_rol_permission(1)
def productos_admnin(request):
    """Vista para mostrar la lista de productos."""
    q = Producto.objects.all()
    breadcrumbs = [
        ("Inicio Admin", reverse("panel_admin")),
        ("lista de productos", reverse("productos_admnin")),
        
    ]
    contexto = { "data": q,
                'breadcrumbs': breadcrumbs,
    }
    return render(request, "administrador/productos/listar_productos.html", contexto)

#-----------------------------------------------------
    # FIN PRODUCTOS ADMINISTRADOR
#-----------------------------------------------------

@session_rol_permission(1)
def aprobar_solicitud_vendedor(request, id_solicitud):
    solicitud = SolicitudVendedor.objects.get(pk=id_solicitud)
    solicitud.estado = 'aprobado'
    solicitud.usuario.rol = 3  # Cambia a vendedor
    solicitud.usuario.save()
    solicitud.save()
    # Crear notificación
    Notificacion.objects.create(
        usuario=solicitud.usuario,
        mensaje="¡Tu solicitud para ser vendedor ha sido aprobada!"
    )
    messages.success(request, "Solicitud aprobada y usuario actualizado a vendedor.")
    return redirect("solicitudes_vendedor")

@session_rol_permission(1)
def rechazar_solicitud_vendedor(request, id_solicitud):
    solicitud = SolicitudVendedor.objects.get(pk=id_solicitud)
    solicitud.estado = 'rechazado'
    solicitud.save()
    # Crear notificación
    Notificacion.objects.create(
        usuario=solicitud.usuario,
        mensaje="Tu solicitud para ser vendedor fue rechazada. Puedes volver a intentarlo."
    )
    messages.info(request, "Solicitud rechazada.")
    return redirect("solicitudes_vendedor")

def notificaciones_usuario(request):
    if request.session.get("pista") and request.session["pista"]["rol"] == 2:
        usuario_id = request.session["pista"]["id"]
        usuario = Usuario.objects.get(pk=usuario_id)
        notificaciones = Notificacion.objects.filter(usuario=usuario).order_by('-fecha')[:10]
        return {"notificaciones_usuario": notificaciones}
    return {"notificaciones_usuario": []}
# -----------------------------------------------------
    # FIN ADMINISTRADOR
# -----------------------------------------------------

# ---------------------------------------------
    ## Carrito de compras
# ---------------------------------------------

def obtener_carrito(request):
    """Obtiene el carrito del usuario autenticado o de la sesión."""
    if request.user.is_authenticated:
        # Buscar el usuario en tu modelo personalizado
        usuario = Usuario.objects.filter(correo=request.user.email).first()
        if not usuario:
            # Crear el usuario automáticamente si no existe
            usuario = Usuario.objects.create(
                nombre_apellido=request.user.get_full_name() or request.user.username,
                correo=request.user.email,
                password=request.user.password,
                rol=2,  # O el rol por defecto que desees
            )
        carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id).first()
            if not carrito:
                messages.info(request, "Tu carrito fue eliminado por inactividad. Se ha creado uno nuevo.")
                carrito = Carrito.objects.create()
                request.session['carrito_id'] = carrito.id
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
    if not producto.stock or producto.stock <= 0:
        messages.error(request, "Este producto ya no está disponible.")
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

@session_rol_permission()
def pagar_carrito(request):
    """Procesa el pago del carrito."""
    carrito = obtener_carrito(request)
    if not carrito.elementos.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('carrito')

    if not carrito.usuario:
        usuario_id = request.session.get("pista", {}).get("id")
        if usuario_id:
            usuario = Usuario.objects.get(pk=usuario_id)
            carrito.usuario = usuario
            carrito.save()
        else:
            messages.error(request, "Debes iniciar sesión para pagar.")
            return redirect('login')

    total = sum(elemento.producto.precio * elemento.cantidad for elemento in carrito.elementos.all())
    usuario = carrito.usuario

    try:
        with transaction.atomic():
            # Verificar stock antes de crear la orden
            for elemento in carrito.elementos.select_related('producto'):
                producto = Producto.objects.select_for_update().get(pk=elemento.producto.pk)
                if elemento.cantidad > producto.stock:
                    messages.error(request, f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
                    return redirect('carrito')

            # Registrar la orden
            orden = Orden.objects.create(usuario=usuario, total=total)
            for elemento in carrito.elementos.all():
                producto = Producto.objects.select_for_update().get(pk=elemento.producto.pk)
                if elemento.cantidad > producto.stock:
                    messages.error(request, f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
                    transaction.set_rollback(True)
                    return redirect('carrito')
                OrdenItem.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad=elemento.cantidad,
                    precio_unitario=producto.precio
                )
                producto.stock = F('stock') - elemento.cantidad
                producto.save()
                elemento.delete()
            carrito.elementos.all().delete()
            messages.success(request, "Pago procesado correctamente.")
    except Exception as e:
        messages.error(request, f"Error al procesar el pago: {e}")
        return redirect('carrito')
    return redirect('index')

def combinar_carritos(request):
    usuario_id = request.session.get("pista", {}).get("id")
    if usuario_id:
        session_carrito_id = request.session.get('carrito_id')
        if session_carrito_id:
            session_carrito = Carrito.objects.filter(id=session_carrito_id).first()
            usuario = Usuario.objects.get(pk=usuario_id)
            user_carrito, _ = Carrito.objects.get_or_create(usuario=usuario)
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
    """Vista para buscar productos por nombre."""
    query = request.GET.get('q', '')  # Obtén el término de búsqueda
    resultados = Producto.objects.filter(nombre__icontains=query) if query else []
    contexto = {
        'data': resultados,  # Pasar los productos encontrados
        'query': query,
        'mostrar_boton_agregar': False,  # Opcional: Ocultar el botón de agregar
    }
    return render(request, 'productos/listar_productos.html', contexto)

